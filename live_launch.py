from flask import Flask, request, jsonify
from pyngrok import ngrok
from core.core_system import CoreSystem
import threading

# ---- Initialize Flask + AI ----
app = Flask(__name__)
ai_brain = CoreSystem()
ai_brain.start()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    success, response = ai_brain.process_cycle(input_text=question)
    return jsonify({"success": success, "response": response})

# ---- Function to run Flask ----
def run_flask():
    print("✔ AI Brain server running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)

# ---- Start Flask in a thread ----
threading.Thread(target=run_flask).start()

# ---- Open Ngrok tunnel ----
public_url = ngrok.connect(5000)
print("🌐 Public URL:", public_url)

# Keep script alive
input("Press ENTER to stop AI Brain and close tunnel...")
ngrok.disconnect(public_url)
ngrok.kill()
