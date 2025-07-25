from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow calls from frontend

# Your ngrok tunnel for Ollama model
OLLAMA_URL = " https://628bb7d72f9f.ngrok-free.app"  # <-- change to your tunnel URL

@app.route('/chat', methods=['POST'])
def chat():
    user_prompt = request.json.get("prompt", "")
    payload = {
        "model": "gemma3:1b",
        "prompt": user_prompt,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    result = response.json()
    return jsonify({"reply": result['response']})

if __name__ == '__main__':
    app.run()
