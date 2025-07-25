from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests  # if you're calling local Ollama

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt', '')

    # Send request to your local Ollama running at home using ngrok or other tunnel
    response = requests.post('https://32b586d98207.ngrok-free.app/api/generate', json={"prompt": prompt})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
