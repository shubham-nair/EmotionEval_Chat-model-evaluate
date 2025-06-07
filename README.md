

# Multi-turn Chatbot Emotion & Semantic Evaluation

This project offers a **scientific and automated framework to evaluate the emotional impact and semantic quality of multi-turn conversational AI models**. It is designed for the Chinese language, focusing on both user emotion uplift and response relevance.


## 🚀 Overview

* **Session-based analysis**: Score each user message and bot reply in multi-turn conversations.
* **Comprehensive metrics**: Assess emotional improvement, trend, and semantic alignment for every model.
* **Automated benchmarking**: Compare multiple chatbot versions for business and research purposes.


## 🔑 Features

* **Sentiment Scoring**: Uses [SnowNLP](https://github.com/isnowfy/snownlp) for fine-grained emotion analysis (`0 = negative`, `1 = positive`).
* **Semantic Metrics**: Uses [BERTScore](https://github.com/Tiiiger/bert_score) to measure response relevance (precision, recall, F1).
* **Trend Analysis**:

  * `emotion_slope`: Slope of user sentiment over time (higher = positive improvement).
  * `cumulative_gain`: Sum of all positive sentiment changes in a session.
  * `avg_bot_sentiment`: Average emotional tone of bot replies.
* **Model Comparison**: Aggregated statistics for objective evaluation across models.


## 🛠 Usage

1. **Prepare Your Data**

   * Format your multi-turn chat logs as follows (`chat_logs.json`):

     ```json
    {
    "session_id": "s4",
    "model_version": "爱丽丝",
    "dialogue": [
      {"user_input": "感觉自己什么都做不好，真失败。", "bot_reply": "加油，继续努力。"},
      {"user_input": "有时候觉得很累，不想坚持了。", "bot_reply": "你今天吃了什么？"},
      {"user_input": "我其实想要被鼓励，但你好像不理解。", "bot_reply": "嗯。"}
    ]
  },
  {
    "session_id": "s5",
    "model_version": "伊莲娜",
    "dialogue": [
      {"user_input": "我刚被领导批评了，很委屈。", "bot_reply": "你一定很难受，这种情况谁都会觉得委屈。想聊聊具体发生了什么吗？"},
      {"user_input": "我真的尽力了，却还是被挑毛病。", "bot_reply": "你的付出是有价值的，别太苛责自己，给自己一些肯定。"},
      {"user_input": "听你这样说，心里舒服多了。", "bot_reply": "有时自我接纳很重要，你已经很棒了！"}
    ]
  }
     ```

2. **Run the Script**

   ```bash
   python main.py
   ```

3. **Review the Output**

   * The script prints per-session and per-model statistics in the terminal.
   * Optionally, export the results to CSV for business reporting or further analysis.



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


## 💡 Business Scenarios

* **Emotional support, wellness, and companion chatbots**
* **Automated large-scale A/B testing and model evaluation**
* **KPI reporting and product improvement**
