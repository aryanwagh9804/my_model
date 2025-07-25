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

    # Send to your local Ollama via ngrok
    try:
        res = requests.post(
            'https://30e9fb5dba8a.ngrok-free.app/api/generate',
            json={"model":"gemma3:1b","prompt": prompt},
            timeout=20
        )
        print("Raw Ollama Response:", res.text)  # 👈 Debugging line

        # Return entire Ollama JSON for now
        return jsonify({"response": res.json()})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Failed to get response from Ollama"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
