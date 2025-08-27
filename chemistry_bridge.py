import os
from flask import Flask, jsonify, request
from openai import OpenAI

# Correct _name_ usage
app = Flask(_name_)

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "✅ Chemistry Bridge is live on Render!"

@app.route("/bridge", methods=["GET"])
def bridge():
    # Get the user's question from query parameter ?q=
    question = request.args.get("q", "Explain a chemistry concept with inspiration.")

    # Call OpenAI with subjective chemist persona
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a world-renowned chemist. "
                           "Answer questions subjectively, with creativity, "
                           "and in the tonality of famous chemists—"
                           "not just textbook definitions."
            },
            {"role": "user", "content": question}
        ]
    )

    final_answer = response.choices[0].message.content
    return jsonify({"answer": final_answer})

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
