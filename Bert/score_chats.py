import json
import pandas as pd
from snownlp import SnowNLP
from scipy.stats import linregress

def analyze_sentiment(text):
    # 取值范围 0（负面）~1（正面）
    return round(SnowNLP(text).sentiments, 4)

def calc_emotion_slope(sentiments):
    if len(sentiments) < 2:
        return 0.0
    x = list(range(len(sentiments)))
    slope, _, _, _, _ = linregress(x, sentiments)
    return round(slope, 4)

def calc_cumulative_gain(sentiments):
    gain = 0
    for i in range(1, len(sentiments)):
        delta = sentiments[i] - sentiments[i-1]
        if delta > 0:
            gain += delta
    return round(gain, 4)

if __name__ == "__main__":
    # 1. 读取多轮对话数据
    with open("Bert/chat_logs.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for session in data:
        # 获取每一轮用户的情绪分
        user_sentiments = [analyze_sentiment(turn["user_input"]) for turn in session["dialogue"]]
        # 也可以分析 bot 回复的情绪分（如果需要）
        bot_sentiments = [analyze_sentiment(turn["bot_reply"]) for turn in session["dialogue"]]

        # 情绪趋势分析
        slope = calc_emotion_slope(user_sentiments)
        cumulative_gain = calc_cumulative_gain(user_sentiments)

        results.append({
            "session_id": session["session_id"],
            "model_version": session["model_version"],
            "start_sentiment": round(user_sentiments[0], 4),
            "end_sentiment": round(user_sentiments[-1], 4),
            "emotion_slope": slope,
            "cumulative_gain": cumulative_gain,
            "turns": len(user_sentiments),
            "avg_bot_sentiment": round(sum(bot_sentiments)/len(bot_sentiments), 4)
        })

    df = pd.DataFrame(results)

    # 2. 输出每个 session 的情绪趋势分析
    print("\n🎯 每个session情绪趋势分析：\n")
    print(df[[
        "session_id", "model_version", "start_sentiment", "end_sentiment",
        "emotion_slope", "cumulative_gain", "avg_bot_sentiment", "turns"
    ]].to_markdown(index=False))

    # 3. 按模型聚合平均值
    summary = df.groupby("model_version")[[
        "emotion_slope", "cumulative_gain", "start_sentiment",
        "end_sentiment", "avg_bot_sentiment"
    ]].mean().round(4)
    summary["count"] = df.groupby("model_version").size()

    print("\n📊 按模型版本的平均情绪提升表现：\n")
    print(summary.reset_index().to_markdown(index=False))

    print("\n字段含义说明：")
    print("""
    | 字段名            | 含义说明                                               |
    |-------------------|------------------------------------------------------|
    | model_version     | 机器人/模型的名称                                      |
    | emotion_slope     | 情绪趋势斜率：数值越高，用户情绪随对话越向正面变化（长期趋势）|
    | cumulative_gain   | 累计正向提升：用户情绪每次提升的累计和，反映过程中的多次小改善|
    | start_sentiment   | 初始情绪分：用户在对话第一轮时的情绪分（0=负面，1=正面）    |
    | end_sentiment     | 结束情绪分：用户在对话最后一轮时的情绪分                 |
    | avg_bot_sentiment | 机器人整体输出的情绪分均值（0=负面，1=正面），反映输出风格   |
    | count             | 该模型下参与统计的 session 数量                         |
    """)

    # 4. 可选：保存为 csv
    # df.to_csv("session_emotion_trends.csv", index=False)
    # summary.to_csv("model_emotion_trends.csv")
