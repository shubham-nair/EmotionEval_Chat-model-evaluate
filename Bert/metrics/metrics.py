import pandas as pd

def session_metrics(session, sentiment_funs, bertscore_fun):
    user_inputs = [turn["user_input"] for turn in session["dialogue"]]
    bot_replies = [turn["bot_reply"] for turn in session["dialogue"]]
    user_sentiments = [sentiment_funs['analyze_sentiment'](u) for u in user_inputs]
    bot_sentiments = [sentiment_funs['analyze_sentiment'](b) for b in bot_replies]
    P, R, F1 = bertscore_fun(user_inputs, bot_replies)
    slope = sentiment_funs['calc_emotion_slope'](user_sentiments)
    cumulative_gain = sentiment_funs['calc_cumulative_gain'](user_sentiments)
    return {
        "session_id": session["session_id"],
        "model_version": session["model_version"],
        "f1_avg": round(sum(F1) / len(F1), 4),
        "precision_avg": round(sum(P) / len(P), 4),
        "recall_avg": round(sum(R) / len(R), 4),
        "start_sentiment": round(user_sentiments[0], 4),
        "end_sentiment": round(user_sentiments[-1], 4),
        "emotion_slope": slope,
        "cumulative_gain": cumulative_gain,
        "avg_bot_sentiment": round(sum(bot_sentiments) / len(bot_sentiments), 4),
        "turns": len(user_inputs)
    }

def to_dataframe(results):
    return pd.DataFrame(results)

def aggregate_summary(df):
    summary = df.groupby("model_version")[[
        "f1_avg", "precision_avg", "recall_avg", "emotion_slope", "cumulative_gain",
        "start_sentiment", "end_sentiment", "avg_bot_sentiment"
    ]].mean().round(4)
    summary["count"] = df.groupby("model_version").size()
    return summary.reset_index()
