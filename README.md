

# Multi-turn Chatbot Emotion & Semantic Evaluation

This project provides an **enterprise-grade, automated evaluation pipeline for multi-turn conversational AI models**, tailored for Chinese-language chatbots. By leveraging PySpark for scalable distributed processing, it enables both scientific benchmarking and business-oriented insight into user emotional uplift and conversational quality.



## 🚀 Overview

* **Production-scale analytics**: Uses [Apache Spark](https://spark.apache.org/) to efficiently process and evaluate large volumes of chat logs across multiple models or experiments.
* **Session-level diagnostics**: Measures both user and bot behaviors on a per-session basis, supporting granular emotional and semantic analysis.
* **Robust benchmarking**: Aggregates statistics for model comparison, A/B test tracking, and continuous deployment decision-making.



## 🔑 Key Features

* **Distributed Sentiment Analysis**: Employs [SnowNLP](https://github.com/isnowfy/snownlp) to score user and bot utterances (`0 = negative`, `1 = positive`) in a scalable, parallelized Spark environment.
* **Semantic Relevance Metrics**: Applies [BERTScore](https://github.com/Tiiiger/bert_score) for in-depth semantic similarity (Precision, Recall, F1), capturing the alignment between user input and bot response.
* **Session-level Trends**:

  * `emotion_slope`: Measures change in user sentiment per session, highlighting emotional improvement or deterioration.
  * `cumulative_gain`: Quantifies total positive emotional changes, reflecting the chatbot's real-world emotional impact.
  * `avg_bot_sentiment`: Captures the emotional tone of the bot's replies.
* **Automated Model Comparison**: Generates aggregated performance reports to enable objective cross-model or version comparison for both business and research.



## 🛠 Usage

### 1. Data Preparation

Prepare your multi-turn conversation logs as a JSON array (`chat_logs.json`), each record containing:

```json
{
  "session_id": "s4",
  "model_version": "Alice",
  "dialogue": [
    { "user_input": "I'm feeling down today.", "bot_reply": "I'm here for you." },
    ...
  ]
}
```

### 2. Run the Evaluation Pipeline

You can run the end-to-end analysis script with:

```bash
python main.py
```

This will automatically convert input to Spark-compatible JSON lines, launch PySpark, and execute distributed computation.

### 3. Review Results

* **Per-session**: Detailed metrics per dialogue session, including emotion trend and semantic quality.
* **Per-model aggregation**: Grouped statistics (mean, count) for each model version, suitable for business dashboarding or experiment tracking.
* **Output**: Results can be saved as Parquet or CSV for integration with BI tools or further analytics.



## ⚡️ Spark-Powered Scalability

* **Big data ready**: Efficiently processes millions of chat sessions in parallel, making it ideal for real-world production or research datasets.
* **Cluster/Cloud deployment**: Seamlessly integrates with Hadoop, YARN, Kubernetes, AWS EMR, or Databricks for enterprise-scale analytics.
* **Extensible**: Easily supports additional metrics (e.g., coherence, custom intent detection) via Spark UDFs.



## 📊 Example Output

| model\_version | f1\_avg | precision\_avg | recall\_avg | emotion\_slope | cumulative\_gain | start\_sentiment | end\_sentiment | avg\_bot\_sentiment | count |
| -------------- | ------- | -------------- | ----------- | -------------- | ---------------- | ---------------- | -------------- | ------------------- | ----- |
| Elena          | 0.6071  | 0.5821         | 0.6353      | 0.0082         | 0.4589           | 0.6698           | 0.6861         | 0.8604              | 4     |
| Alice          | 0.5851  | 0.6115         | 0.5620      | -0.0275        | 0.1555           | 0.6968           | 0.6419         | 0.5873              | 4     |

**Field Descriptions:**

| Field               | Description                                            |
| ------------------- | ------------------------------------------------------ |
| model\_version      | Name of the chatbot/model                              |
| f1\_avg             | BERTScore F1 (semantic similarity, higher is better)   |
| precision\_avg      | BERTScore Precision (average)                          |
| recall\_avg         | BERTScore Recall (average)                             |
| emotion\_slope      | Slope of user sentiment trend (positive = improvement) |
| cumulative\_gain    | Total positive sentiment gain across a session         |
| start\_sentiment    | Sentiment score at the start of the session            |
| end\_sentiment      | Sentiment score at the end of the session              |
| avg\_bot\_sentiment | Average sentiment of all bot replies                   |
| count               | Number of sessions per model                           |



## 💡 Business & Research Applications

* **Conversational AI product evaluation**: Essential for companion, wellness, or psychological support bots where emotional impact matters.
* **Large-scale model benchmarking**: Enables robust A/B/N experiments, model release validation, and regression detection.
* **Automated reporting**: Supports integration with BI dashboards (e.g., Metabase, Tableau) for executive or research monitoring.
* **Continuous optimization**: Designed for daily/weekly pipeline runs, enabling ongoing model and product improvement.



## 🌏 Why Spark?

By leveraging PySpark, this project overcomes the scale and speed limitations of local scripts, unlocking real-time analytics and automated insights for both small and massive chatbot datasets. **Deploy once, scale on demand**—no change needed for single-machine prototyping or production-grade distributed analytics.

