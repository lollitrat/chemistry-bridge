import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(_name_)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "✅ Chemistry Bridge is running on Render!"

@app.route("/bridge", methods=["GET"])
def bridge():
    # Get user question from query parameter
    user_question = request.args.get("q", "Explain something about chemistry.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a famous chemist giving subjective, inspiring answers."},
            {"role": "user", "content": user_question}
        ]
    )

    final_answer = response.choices[0].message.content
    return jsonify({"answer": final_answer})

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
