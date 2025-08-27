import os
from flask import Flask, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "✅ Chemistry Bridge is running on Render!"

@app.route("/bridge")
def bridge():
    prompt = "You are a world-renowned chemist..."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a famous chemist giving subjective, inspiring answers."},
            {"role": "user", "content": prompt}
        ]
    )
    final_answer = response.choices[0].message.content
    return jsonify({"answer": final_answer})

if _name_ == "_main_":   # ✅ double underscores
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
