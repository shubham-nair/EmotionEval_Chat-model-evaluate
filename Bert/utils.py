import json
import pandas as pd

def load_chat_logs(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def print_df(df):
    print("\n==== 打分结果 ====\n")
    print(df.to_markdown(index=False))
