from data_loader_chatlogs import load_data
from eval_fed_gpt import eval_fed
import pandas as pd

if __name__ == "__main__":
    # 1. 加载聊天记录并转换为 FED 格式
    data = load_data()

    # 2. 调用 GPT 评分函数
    scores = eval_fed(data)

    # 3. 打印每条评分结果
    for s in scores:
        print(s)

    # 4. 保存为 CSV 文件
    df = pd.DataFrame(scores)
    df.to_csv("scored_chat_logs.csv", index=False)
    print("\n✅ 打分结果已保存为 scored_chat_logs.csv")
