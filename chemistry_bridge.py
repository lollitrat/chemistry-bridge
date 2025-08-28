import os
from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "✅ Chemistry Bridge is live!"

@app.route("/bridge", methods=["POST"])
def bridge():
    try:
        # Parse JSON input
        data = request.get_json(force=True)
        query = data.get("query", "Explain a chemistry concept.")
        chemist = data.get("chemist", "Marie Curie")

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are {chemist}, a world-renowned chemist. "
                               f"Answer questions creatively in your own style."
                },
                {"role": "user", "content": query}
            ]
        )

        final_answer = response.choices[0].message.content

        # ✅ Schema-safe response
        return jsonify({
            "messages": [
                {
                    "type": "text",
                    "content": final_answer
                }
            ]
        })

    except Exception as e:
        # Even errors are schema-safe
        return jsonify({
            "messages": [
                {
                    "type": "text",
                    "content": f"⚠️ Error: {str(e)}"
                }
            ]
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
