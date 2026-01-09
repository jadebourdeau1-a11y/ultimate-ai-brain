from flask import Flask, request, jsonify
from core.core_system import CoreSystem

app = Flask(__name__)
ai_brain = CoreSystem()
ai_brain.start()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    success, response = ai_brain.process_cycle(input_text=question)
    return jsonify({"success": success, "response": response})

if __name__ == "__main__":
    print("✔ AI Brain live server running on port 5000")
    app.run(host="0.0.0.0", port=5000)
