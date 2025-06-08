import json
import pandas as pd
from Utils.sentiment_utils import analyze_sentiment, calc_emotion_slope, calc_cumulative_gain
from Utils.bertscore_utils import evaluate_bertscore
from metrics.metrics import session_metrics, to_dataframe, aggregate_summary

if __name__ == "__main__":

    with open("Logs/chat_logs.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    sentiment_funs = {
        'analyze_sentiment': analyze_sentiment,
        'calc_emotion_slope': calc_emotion_slope,
        'calc_cumulative_gain': calc_cumulative_gain
    }

    results = [
        session_metrics(session, sentiment_funs, evaluate_bertscore)
        for session in data
    ]
    df = to_dataframe(results)

    print("\n🎯 Per-session Emotion and Semantic Analysis:\n")
    print(df[[
        "session_id", "model_version", "f1_avg", "precision_avg", "recall_avg",
        "start_sentiment", "end_sentiment",
        "emotion_slope", "cumulative_gain", "avg_bot_sentiment", "turns"
    ]].to_markdown(index=False))
    summary = aggregate_summary(df)
    print("\n📊 Model-wise Average Emotion & Semantic Performance:\n")
    print(summary.to_markdown(index=False))


    print("\nField Description:")
    print("""
| Field            | Description                                        |
|------------------|---------------------------------------------------|
| model_version    | Name of chatbot/model                             |
| f1_avg           | BERTScore F1 (semantic similarity, higher=better) |
| precision_avg    | BERTScore Precision (average)                     |
| recall_avg       | BERTScore Recall (average)                        |
| emotion_slope    | Slope of emotion trend (positive=improvement)     |
| cumulative_gain  | Cumulative positive emotion gain                  |
| start_sentiment  | Initial user sentiment                            |
| end_sentiment    | Final user sentiment                              |
| avg_bot_sentiment| Avg. bot reply sentiment                          |
| count            | Sessions per model                                |
    """)

    # Optionally save
    # df.to_csv("session_emotion_and_bertscore.csv", index=False)
    # summary.to_csv("model_emotion_and_bertscore.csv")
