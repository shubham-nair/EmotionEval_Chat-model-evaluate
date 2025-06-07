import os
import json
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, FloatType, StringType

# ========================
# 1. 为测试spark运行效果，先使用本地文件读取转化成spark需要的json格式。
# ========================
raw_json_path = "../Logs/chat_logs.json"
lines_json_path = "../Logs/chat_logs_lines.json"

def convert_json_to_lines(src, dst):
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if content.startswith('['):
            data = json.loads(content)
        else:
            return
    with open(dst, 'w', encoding='utf-8') as fout:
        for record in data:
            fout.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(f"已生成标准 json lines 文件: {dst}")

if not os.path.exists(lines_json_path):
    convert_json_to_lines(raw_json_path, lines_json_path)
    json_path_to_use = lines_json_path
else:
    json_path_to_use = lines_json_path

# ========================
# 2. 初始化 Spark
# ========================
spark = SparkSession.builder.appName("ChatEvalLocal").getOrCreate()

# ========================
# 3. 读取数据
# ========================
df = spark.read.json(json_path_to_use)
df.show(3)
df.printSchema()

# ========================
# 4. 分析逻辑
# ========================
from bert_score import score as bert_score
from snownlp import SnowNLP
from scipy.stats import linregress

def analyze_sentiment(text):
    try:
        return float(round(SnowNLP(text).sentiments, 4))
    except Exception:
        return 0.5

def calc_emotion_slope(sentiments):
    if len(sentiments) < 2:
        return 0.0
    x = list(range(len(sentiments)))
    slope, _, _, _, _ = linregress(x, sentiments)
    return float(round(slope, 4))

def calc_cumulative_gain(sentiments):
    gain = 0.0
    for i in range(1, len(sentiments)):
        delta = float(sentiments[i]) - float(sentiments[i-1])
        if delta > 0:
            gain += delta
    return float(round(gain, 4))

def evaluate_bertscore(user_inputs, bot_replies):
    if not user_inputs or not bot_replies:
        return [0.0], [0.0], [0.0]
    P, R, F1 = bert_score(bot_replies, user_inputs, lang="zh", verbose=False)

    return list(map(float, P.tolist())), list(map(float, R.tolist())), list(map(float, F1.tolist()))

def session_metrics_spark(row):
    try:
        dialogue = getattr(row, "dialogue", []) or []
        user_inputs = [getattr(t, "user_input", "") for t in dialogue]
        bot_replies = [getattr(t, "bot_reply", "") for t in dialogue]
        user_sentiments = [analyze_sentiment(u) for u in user_inputs]
        bot_sentiments = [analyze_sentiment(b) for b in bot_replies]

        P, R, F1 = evaluate_bertscore(user_inputs, bot_replies) if user_inputs and bot_replies else ([0.0],[0.0],[0.0])

        f1_avg = float(round(sum(F1)/len(F1), 4)) if F1 else 0.0
        precision_avg = float(round(sum(P)/len(P), 4)) if P else 0.0
        recall_avg = float(round(sum(R)/len(R), 4)) if R else 0.0
        start_sentiment = float(round(user_sentiments[0], 4)) if user_sentiments else 0.0
        end_sentiment = float(round(user_sentiments[-1], 4)) if user_sentiments else 0.0
        slope = calc_emotion_slope(user_sentiments)
        cumulative_gain = calc_cumulative_gain(user_sentiments)
        avg_bot_sentiment = float(round(sum(bot_sentiments)/len(bot_sentiments), 4)) if bot_sentiments else 0.0
        turns = float(len(user_inputs))

        return (
            getattr(row, "session_id", None),
            getattr(row, "model_version", None),
            f1_avg,
            precision_avg,
            recall_avg,
            start_sentiment,
            end_sentiment,
            slope,
            cumulative_gain,
            avg_bot_sentiment,
            turns
        )
    except Exception as e:
        print("Error:", e)
        return (None, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

# ========================
# 5. 注册 UDF
# ========================
schema = StructType([
    StructField("session_id", StringType(), True),
    StructField("model_version", StringType(), True),
    StructField("f1_avg", FloatType(), True),
    StructField("precision_avg", FloatType(), True),
    StructField("recall_avg", FloatType(), True),
    StructField("start_sentiment", FloatType(), True),
    StructField("end_sentiment", FloatType(), True),
    StructField("emotion_slope", FloatType(), True),
    StructField("cumulative_gain", FloatType(), True),
    StructField("avg_bot_sentiment", FloatType(), True),
    StructField("turns", FloatType(), True),
])
metrics_udf = F.udf(session_metrics_spark, schema)

# ========================
# 6. UDF 逐条分析
# ========================
result_df = df.withColumn("metrics", metrics_udf(F.struct([df[x] for x in df.columns])))
flat_df = result_df.select("metrics.*")
flat_df.show(3)

# ========================
# 7. 按模型聚合
# ========================
summary_df = flat_df.groupBy("model_version").agg(
    F.avg("f1_avg").alias("f1_avg_mean"),
    F.avg("precision_avg").alias("precision_avg_mean"),
    F.avg("recall_avg").alias("recall_avg_mean"),
    F.avg("emotion_slope").alias("emotion_slope_mean"),
    F.avg("cumulative_gain").alias("cumulative_gain_mean"),
    F.avg("start_sentiment").alias("start_sentiment_mean"),
    F.avg("end_sentiment").alias("end_sentiment_mean"),
    F.avg("avg_bot_sentiment").alias("avg_bot_sentiment_mean"),
    F.count("*").alias("session_count")
)
summary_df.show()

# ========================
# 8. 保存分析结果
# ========================
flat_df.write.mode("overwrite").parquet("./emotion_eval_per_session/")
summary_df.write.mode("overwrite").parquet("./emotion_eval_model_summary/")

print("分析结果已导出：./emotion_eval_per_session/  和  ./emotion_eval_model_summary/")
