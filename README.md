
# Multi-turn Chatbot Emotion Evaluation

This project provides a **scientific framework for evaluating the emotional improvement capabilities of multi-turn conversational AI models**. It supports automatic sentiment analysis, trend measurement, and model comparison for Chinese language chatbot conversations.

## 🚀 Project Overview

- Analyze **multi-turn (session-based) dialogues**, with sentiment scoring for each user input and bot reply
- Focus on **core business metrics** such as user emotion uplift and emotional support effectiveness
- Automatically generate both per-session and model-level comparison reports for business and research use

## 🔑 Key Features

- **Sentiment Scoring**: Uses [SnowNLP](https://github.com/isnowfy/snownlp) for sentiment analysis of each user utterance and bot reply (`0 = negative`, `1 = positive`)
- **Trend Metrics**:
  - `emotion_slope`: Slope of user sentiment trend over the session (positive = improving)
  - `cumulative_gain`: Total sum of all positive sentiment improvements in a session
  - `avg_bot_sentiment`: Average sentiment score of all bot replies
- **Model Comparison**: Aggregate statistics per model version for objective benchmarking

## 🛠 How to Use

1. **Prepare Data**  
   Save your multi-turn chat data in the following structure as `chat_logs.json`:
   
   ```json
   [
     {
       "session_id": "s1",
       "model_version": "Elena",
       "dialogue": [
         {"user_input": "I'm feeling down today.", "bot_reply": "It's okay, you're not alone. Everyone has tough days. Tomorrow will be better."}
         // ... more turns
       ]
     }
     // ... more sessions
   ]
```

2. **Run the Analysis Script**

   ```bash
   python score_chats.py
   ```

3. **Check Results**
   The script prints session-level emotion trend analysis and model-level aggregate results to the terminal. You can also export results to CSV for further analysis or business reporting.

## 📊 Example Output

| model\_version | emotion\_slope | cumulative\_gain | start\_sentiment | end\_sentiment | avg\_bot\_sentiment | count |
| -------------- | -------------- | ---------------- | ---------------- | -------------- | ------------------- | ----- |
| Elena          | 0.0082         | 0.4589           | 0.6698           | 0.6861         | 0.8604              | 4     |
| Alice          | -0.0275        | 0.1555           | 0.6968           | 0.6419         | 0.5873              | 4     |

Field explanations are available in the code comments.

## 💡 Business Value

* Ideal for evaluating conversational AI models in companion, wellness, or psychological support scenarios
* Enables automated large-scale experiments, model deployment decisions, and continuous A/B optimization


