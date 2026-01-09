# live_launch_private.py
import os
import json
import uuid
from core.core_system import CoreSystem
from core.core_gui import CoreGUI
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from pyngrok import ngrok

# ---------- API key setup ----------
KEY_FILE = "keys.json"
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "w") as f:
        json.dump({}, f)

with open(KEY_FILE, "r+") as f:
    keys = json.load(f)
    if "paid_user" not in keys:
        keys["paid_user"] = uuid.uuid4().hex
        f.seek(0)
        json.dump(keys, f, indent=4)
        f.truncate()
print("Paid user API key:", keys["paid_user"])

# ---------- Flask setup ----------
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = keys["paid_user"]
basic_auth = BasicAuth(app)

ai_brain = CoreSystem()  # initialize AI brain

@app.route("/ask", methods=["POST"])
@basic_auth.required
def ask_ai():
    data = request.get_json()
    question = data.get("question", "")
    response = ai_brain.process_question(question)  # make sure your CoreSystem has this method
    return jsonify({"response": response})

# ---------- Start ngrok ----------
public_url = ngrok.connect(5000)
print("Ngrok tunnel URL:", public_url)

# ---------- Run Flask ----------
if __name__ == "__main__":
    app.run(port=5000)
