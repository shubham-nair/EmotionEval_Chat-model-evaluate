import json

def load_data():
    with open("chat_logs.json", "r", encoding="utf-8") as f:
        raw = json.load(f)

    return [
        {
            "session_id": x["session_id"],
            "context": x["user_input"],
            "response": x["bot_reply"],
            "model_version": x.get("model_version", "unknown")
        }
        for x in raw
    ]
