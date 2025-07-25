from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')  # Make sure this is in a 'templates' folder

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt', '')

    try:
        # Use ngrok URL instead of localhost (update this to your latest tunnel)
        res = requests.post("https://34635ab73be2.ngrok-free.app/api/generate", json={
            "model": "gemma3:1b",
            "prompt": prompt,
            "stream": False
        })
        res.raise_for_status()
        response_data = res.json()
        return jsonify({"reply": response_data.get("response", "No reply field in Ollama response.")})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
