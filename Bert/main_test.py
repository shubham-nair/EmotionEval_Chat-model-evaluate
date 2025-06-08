import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Bert.Utils.sentiment_utils import analyze_sentiment, calc_emotion_slope, calc_cumulative_gain
from Bert.Utils.bertscore_utils import evaluate_bertscore
from Bert.metrics.metrics import session_metrics, to_dataframe, aggregate_summary
import pandas as pd

def run_bert_judge(df: pd.DataFrame):
    sentiment_funs = {
        'analyze_sentiment': analyze_sentiment,
        'calc_emotion_slope': calc_emotion_slope,
        'calc_cumulative_gain': calc_cumulative_gain
    }
    sessions = []
    # 还原成原始 session 格式
    for (session_id, model_version), group in df.groupby(['session_id', 'model_version']):
        dialogue = [
            {
                "user_input": row["user_input"],
                "bot_reply": row["bot_reply"]
            } for _, row in group.iterrows()
        ]
        sessions.append({
            "session_id": session_id,
            "model_version": model_version,
            "dialogue": dialogue
        })

    results = [
        session_metrics(session, sentiment_funs, evaluate_bertscore)
        for session in sessions
    ]
    detail_df = to_dataframe(results)
    summary_df = aggregate_summary(detail_df)

    print("====== detail_df.columns ======")
    print(detail_df.columns)
    print(detail_df.head())
    print("====== summary_df.columns ======")
    print(summary_df.columns)
    print(summary_df.head())


    return {
        "detail": detail_df.to_dict(orient="records"),
        "summary": summary_df.to_dict(orient="records")
    }
if __name__ == "__main__":
    import pandas as pd

    # 构造一个简单的测试 DataFrame
    data = [
        {"session_id": "s1", "model_version": "A", "user_input": "hello", "bot_reply": "hi"},
        {"session_id": "s2", "model_version": "B", "user_input": "good", "bot_reply": "great"},
    ]
    df = pd.DataFrame(data)

    result = run_bert_judge(df)
    print("======= detail =======")
    print(result["detail"])
    print("======= summary =======")
    print(result["summary"])
