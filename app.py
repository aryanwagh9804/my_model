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

    try:
        ollama_url = 'https://30e9fb5dba8a.ngrok-free.app/api/generate'
        res = requests.post(ollama_url, json={"prompt": prompt}, timeout=20)

        print("Status Code:", res.status_code)
        print("Raw Response:", res.text)

        response_data = res.json()
        return jsonify({"reply": response_data.get("response", "No reply field in Ollama response.")})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": "No reply received or error!"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
