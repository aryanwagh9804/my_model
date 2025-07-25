@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt', '')

    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    })

    response_data = res.json()
    return jsonify({"reply": response_data.get("response", "No reply field in Ollama response.")})
