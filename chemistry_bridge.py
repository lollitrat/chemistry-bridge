from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# OpenAI client (reads your key from Render env var)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return "Chemistry Bridge is running!"

@app.post("/ask")
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    chemist = (data.get("chemist") or "").strip()

    if not question:
        return jsonify({"error": "Missing 'question'"}), 400

    # Build the persona
    chemist_desc = f"the chemist {chemist} (write in their style without claiming to be them)" \
                   if chemist else "a famous chemist"
    system_msg = (
        f"You are an expert chemistry tutor speaking in the style of {chemist_desc}. "
        "Give concise, insightful explanations with a subjective first-person tone when helpful. "
        "Use plain language; include key equations/reactions inline if they help. "
        "If you assume anything, say it explicitly."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": question},
    ]

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
        )
        answer = resp.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
