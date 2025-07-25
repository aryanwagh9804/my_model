from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt', '')

    # Fixed URL (no leading space)
    ollama_url = 'https://19cd6a723517.ngrok-free.app/api/generate'

    # Payload MUST include model name
    payload = {
        "model": "gemma3:1b",   # or whatever model you're using
        "prompt": prompt
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=20)

        # Safely decode JSON only if status is OK
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "error": "Ollama returned an error",
                "status": response.status_code,
                "text": response.text
            })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to connect to Ollama backend"
        })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
