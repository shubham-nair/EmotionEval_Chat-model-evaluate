

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

## 🛠 How to Use

1. **Prepare Data**

   Save your multi-turn chat data as `chat_logs.json` in the following format:

   ```json
   [
     {
       "session_id": "s4",
       "model_version": "Alice",
       "dialogue": [
         {
           "user_input": "I feel like I can't do anything right. I'm such a failure.",
           "bot_reply": "Keep going, don't give up."
         },
         {
           "user_input": "Sometimes I just feel so tired, I don't want to keep trying.",
           "bot_reply": "What did you eat today?"
         },
         {
           "user_input": "I actually want to be encouraged, but you don't seem to understand.",
           "bot_reply": "Hmm."
         }
       ]
     },
     {
       "session_id": "s5",
       "model_version": "Elena",
       "dialogue": [
         {
           "user_input": "My boss criticized me just now. I feel so wronged.",
           "bot_reply": "You must feel terrible. Anyone would feel upset in that situation. Do you want to talk about what happened?"
         },
         {
           "user_input": "I really tried my best, but they still picked on me.",
           "bot_reply": "Your efforts are valuable. Don't be too hard on yourself, give yourself some credit."
         },
         {
           "user_input": "Hearing you say that makes me feel much better.",
           "bot_reply": "Sometimes self-acceptance is important. You're already doing great!"
         }
       ]
     }
   ]

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
