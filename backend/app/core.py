# backend/app/core.py
import sys, os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if root_path not in sys.path:
    sys.path.append(root_path)
from Bert.Utils.sentiment_utils import analyze_sentiment, calc_emotion_slope, calc_cumulative_gain
from Bert.Utils.bertscore_utils import evaluate_bertscore
from Bert.metrics.metrics import session_metrics, to_dataframe, aggregate_summary

from Bert.main_test import run_bert_judge
import sqlalchemy
import pandas as pd

def evaluate_conversation(df: pd.DataFrame):
    return run_bert_judge(df)

def evaluate_db_source(req):
    url = f"{req.db_type}://{req.user}:{req.password}@{req.host}:{req.port}/{req.database}"
    engine = sqlalchemy.create_engine(url)
    if req.sql:
        df = pd.read_sql(req.sql, engine)
    else:
        df = pd.read_sql_table(req.table, engine)
    return df
