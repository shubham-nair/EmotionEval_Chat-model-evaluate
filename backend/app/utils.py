# backend/app/utils.py
def check_columns(df, required_cols):
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"缺少字段: {missing}")
    return True

def to_csv_download(df):
    return df.to_csv(index=False, encoding="utf-8")
