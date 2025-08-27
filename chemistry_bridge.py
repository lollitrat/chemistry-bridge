from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/bridge", methods=["POST"])
def bridge():
    user_query = request.json.get("query", "")
    db_answer = request.json.get("db_answer", "")

    # Always rewrite the answer in the tonality of a famous chemist
    prompt = f"""
    You are a world-renowned chemist. 
    The user asked: "{user_query}"
    The database provided this information: "{db_answer}"

    Respond in the voice of a brilliant chemist, adding context, subjective perspective, 
    and making the explanation inspiring while still accurate.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a famous chemist giving subjective, inspiring answers."},
            {"role": "user", "content": prompt}
        ]
    )

    final_answer = response.choices[0].message.content
    return jsonify({"answer": final_answer})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
