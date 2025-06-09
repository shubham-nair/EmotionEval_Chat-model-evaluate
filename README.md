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
| count            | Sessions per model  

## ⚡️ Why Spark?

* **Massive Scale**: Easily handles millions of conversations for enterprise or research.
* **Unified Analytics**: Data cleaning, metrics computation, aggregation—all in one, parallelized.
* **Seamless Cloud/Cluster Support**: Works on AWS EMR, Databricks, on-prem Hadoop, or your laptop with zero code changes.



## 🧑‍💻 Architecture

* **Data Ingestion**: Supports S3, HDFS, local FS.
* **Computation**: Spark UDF for metric extraction; supports further expansion (e.g., coherence, intent accuracy).
* **Output**: Parquet/CSV for BI/ML, real-time reporting, or historical model tracking.


## 🌐 FastAPI Backend Server

This project also includes a FastAPI backend server located in the `Backend/` directory, designed for real-time evaluation of chat interactions via API endpoints. It uses a lightweight SentenceTransformer model for efficient semantic similarity calculation.

### 1. Setup Environment (using uv)

It's recommended to use `uv` for fast virtual environment creation and package installation.

```bash
# Navigate to the project root directory
cd /path/to/EmotionEval_Chat-model-evaluate

# Create a virtual environment using uv (e.g., named .venv)
uv venv .venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows (Command Prompt/PowerShell):
# .venv\Scripts\activate
```

### 2. Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
# Ensure you are in the project root directory where requirements.txt is located
uv pip install -r requirements.txt
```
This will install all necessary dependencies, including `fastapi` and `uvicorn[standard]` for the server.

### 3. Run the FastAPI Server

From the project root directory (with the virtual environment activated):

```bash
uvicorn Backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

*   `--host 0.0.0.0`: Makes the server accessible from your network.
*   `--port 8000`: Runs the server on port 8000.
*   `--reload`: Enables auto-reload when code changes are detected (useful for development).

The API documentation (Swagger UI) will be available at `http://localhost:8000/docs` or `http://your-server-ip:8000/docs`.



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



---

# 🖥️ FastAPI Backend for Model Evaluation (API)

This repo now includes a production-ready FastAPI backend for chat/emotion evaluation, supporting asynchronous preloading of the BERT model/tokenizer for fast first request performance.

## Features
- FastAPI backend for chat/emotion evaluation
- Asynchronous preloading of BERT model/tokenizer at startup for fast first request
- Compatible with EC2 deployment

## Backend Requirements
See `requirements.txt` for all dependencies. Key packages:
- fastapi
- uvicorn
- pandas
- bert-score (for semantic evaluation)
- snownlp
- scipy
- pydantic
- sqlalchemy

## Setup & Usage (Backend)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the backend:**
   ```bash
   uvicorn Backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   On first startup, the backend asynchronously preloads the BERT model/tokenizer for Chinese (zh) using a dummy call. You will see a message like `Model and tokenizer preloaded.` in the logs.

3. **API Usage:**
   - Upload a file to `/evaluate/file` (see API docs at `/docs`).
   - The first request after startup will be fast, with no cold start lag.

## EC2 Hosting Notes
- Ensure ports are open in your EC2 security group (default: 8000).
- Python 3.8+ recommended.
- All dependencies are installable via pip.
- For production, consider running with a process manager (e.g., systemd, supervisor, or Docker).

## Change Log
- 2025-06-08: Added async model/tokenizer preloading at FastAPI startup for efficient serving.
- Updated requirements.txt to include `bert-score` and pin major versions for reliability.
