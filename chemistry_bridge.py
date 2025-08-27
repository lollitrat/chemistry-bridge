import os
from flask import Flask

app = Flask(_name_)

@app.route("/")
def home():
    return "✅ Chemistry Bridge minimal test is running on Render!"

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
