from data_loader_chatlogs import load_data
from eval_fed_gpt import eval_fed
import pandas as pd

def compare_scores_inline():
    # 1. 加载聊天记录（每条包含 session_id, context, response, model_version）
    data = load_data()

    # 2. GPT 评分
    scores = eval_fed(data)

    # 3. 转为 DataFrame
    df = pd.DataFrame(scores)

    # 4. 分组对比模型平均得分
    grouped = df.groupby("model_version")[["fluency", "relevance", "humanness"]].mean().round(2)
    grouped["count"] = df.groupby("model_version").size()

    # 5. 打印每条原始评分
    print("\n🎯 每条评分结果：")
    print(df.to_markdown(index=False))

    # 6. 打印模型对比结果
    print("\n✅ 模型平均评分对比：\n")
    print(grouped.reset_index().to_markdown(index=False))

    # 可选：保存为 CSV（如仍想保留）
    # df.to_csv("scored_chat_logs.csv", index=False)
    # grouped.to_csv("model_comparison.csv")

if __name__ == "__main__":
    compare_scores_inline()
