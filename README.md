# EmotionEval: Large-Scale Multi-turn Chatbot Emotion & Semantic Evaluation

**EmotionEval** delivers a scalable, automated evaluation pipeline for Chinese multi-turn conversational AI. It combines fine-grained emotion analysis and semantic relevance scoring, powered by PySpark for production-grade, big data applications.



## 🚀 Project Highlights

* **Distributed by Design**: Built on PySpark, EmotionEval is ready for millions of chat sessions—run locally or on any Spark/YARN/EMR/Kubernetes cluster.
* **Session-Level Analytics**: Provides per-dialogue and per-turn emotion trajectory and response relevance metrics.
* **Model Version Benchmarking**: Aggregates statistics for business/academic model comparison, A/B/N experiments, and continuous improvement.



## 🔥 Key Features

* **Emotion Analysis**: Uses [SnowNLP](https://github.com/isnowfy/snownlp) for per-utterance sentiment (0=negative, 1=positive), trend slope, and cumulative gain.
* **Semantic Quality**: Leverages [BERTScore](https://github.com/Tiiiger/bert_score) for contextual relevance between user and bot at each turn.
* **Spark-native Automation**: Data loading, metrics computation, and model-wise aggregation are all fully parallelized with Spark, handling everything from notebook prototyping to cluster-scale pipelines.
* **Plug-and-play**: Accepts industry-standard JSONL chat logs; outputs clean metrics for downstream BI or ML pipelines.



## 💡 Typical Scenarios

* **Companion AI and Wellness Bots**: Quantitatively assess a bot’s real impact on user emotions—essential for mental health, wellness, and support products.
* **Automated Model Evaluation**: Run daily/weekly pipeline jobs for regression testing, new model releases, and ongoing experiment tracking.
* **Business Decision Support**: Seamless integration with business dashboards (e.g., Metabase, Tableau) via Parquet/CSV; enables data-driven go/no-go for A/B test launches and KPI monitoring.



## 🛠️ Quick Start

### 1. Prepare Chat Data

Format your logs as JSON or JSON lines (`chat_logs.json`):

```json
[
  {
    "session_id": "s1",
    "model_version": "Alice",
    "dialogue": [
      {"user_input": "I'm exhausted today.", "bot_reply": "Take it easy, you deserve a break."},
      ...
    ]
  }
]
```

### 2. Run Evaluation

```bash
python main.py
```

* Data is automatically converted to Spark-friendly format.
* All computations are parallelized—works out-of-the-box from laptops to clusters.

### 3. Review Output

* Per-session metrics and model-wise summary tables are printed and saved (`Parquet/CSV`).
* Connect your favorite BI tool for interactive analytics.



## 📊 Example Output

| model\_version | f1\_avg | precision\_avg | recall\_avg | emotion\_slope | cumulative\_gain | start\_sentiment | end\_sentiment | avg\_bot\_sentiment | count |
| -------------- | ------- | -------------- | ----------- | -------------- | ---------------- | ---------------- | -------------- | ------------------- | ----- |
| Elena          | 0.6071  | 0.5821         | 0.6353      | 0.0082         | 0.4589           | 0.6698           | 0.6861         | 0.8604              | 4     |
| Alice          | 0.5851  | 0.6115         | 0.5620      | -0.0275        | 0.1555           | 0.6968           | 0.6419         | 0.5873              | 4     |



## ⚡️ Why Spark?

* **Massive Scale**: Easily handles millions of conversations for enterprise or research.
* **Unified Analytics**: Data cleaning, metrics computation, aggregation—all in one, parallelized.
* **Seamless Cloud/Cluster Support**: Works on AWS EMR, Databricks, on-prem Hadoop, or your laptop with zero code changes.



## 🧑‍💻 Architecture

* **Data Ingestion**: Supports S3, HDFS, local FS.
* **Computation**: Spark UDF for metric extraction; supports further expansion (e.g., coherence, intent accuracy).
* **Output**: Parquet/CSV for BI/ML, real-time reporting, or historical model tracking.



## 📦 Requirements

* Python 3.8+
* [PySpark](https://spark.apache.org/)
* [SnowNLP](https://github.com/isnowfy/snownlp)
* [BERTScore](https://github.com/Tiiiger/bert_score)
* [scipy](https://scipy.org/)
* [pandas](https://pandas.pydata.org/)



## 💼 Business Impact

EmotionEval empowers teams to:

* Scientifically measure **user emotion uplift** and **chatbot quality** at scale.
* Automate and **standardize model comparisons** across product releases.
* Support **continuous experimentation** for emotional AI products.


