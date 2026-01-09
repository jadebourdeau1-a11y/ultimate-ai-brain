from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from pyngrok import ngrok
from core.core_system import CoreSystem
import threading

# ---- Flask setup ----
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'user'       # change this
app.config['BASIC_AUTH_PASSWORD'] = 'mypassword' # change this
basic_auth = BasicAuth(app)

ai_brain = CoreSystem()
ai_brain.start()

@app.route("/ask", methods=["POST"])
@basic_auth.required
def ask():
    data = request.json
    question = data.get("question", "")
    success, response = ai_brain.process_cycle(input_text=question)
    return jsonify({"success": success, "response": response})

# ---- Flask thread ----
def run_flask():
    print("✔ AI Brain server running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)

threading.Thread(target=run_flask).start()

# ---- Ngrok ----
public_url = ngrok.connect(5000)
print("🌐 Public URL:", public_url)
print("⚠ Use Basic Auth: user/mypassword")

input("Press ENTER to stop AI Brain and close tunnel...")
ngrok.disconnect(public_url)
ngrok.kill()
