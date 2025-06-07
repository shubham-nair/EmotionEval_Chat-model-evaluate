import openai
import os
import json
import time
from openai import OpenAI
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def format_prompt(context, response):
    return f"""用户输入：“{context}”
机器人回复：“{response}”

请按以下三个维度为机器人的回复打分（每项 0~5 分）：
1. 回复是否流畅自然（fluency）？
2. 回复是否与用户输入相关（relevance）？
3. 回复是否像人类而非机器人所说（humanness）？

请直接输出标准 JSON 格式：
{{"fluency": 4.8, "relevance": 4.5, "humanness": 4.6}}"""

def gpt_score(prompt, model="gpt-4"):
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            text = response.choices[0].message.content
            return json.loads(text)
        except Exception as e:
            print(f"重试中（第{attempt+1}次）... 错误：{e}")
            time.sleep(2)
    return {"fluency": 0, "relevance": 0, "humanness": 0}

def eval_fed(data):
    results = []
    for item in data:
        prompt = format_prompt(item["context"], item["response"])
        scores = gpt_score(prompt)
        results.append({
            "session_id": item["session_id"],
            "model_version": item.get("model_version", "unknown"),  # 🔧 加入模型版本字段
            **scores
        })
    return results

