from flask import Flask, request, jsonify
from flask_cors import CORS
import requests  # if you're calling local Ollama

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Flask server is live!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt', '')

    # Send request to your local Ollama running at home using ngrok or other tunnel
    response = requests.post('https://628bb7d72f9f.ngrok-free.app/api/generate', json={"prompt": prompt})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
