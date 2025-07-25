@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt', '')

    try:
        # Remove extra space before URL if there is any
        ollama_url = 'https://30e9fb5dba8a.ngrok-free.app/api/generate'

        res = requests.post(ollama_url, json={"prompt": prompt}, timeout=20)

        print("Status Code:", res.status_code)
        print("Raw Response:", res.text)

        # Try parsing response
        response_data = res.json()
        return jsonify({"reply": response_data.get("response", "No reply field in Ollama response.")})

    except Exception as e:
        print("ERROR:", str(e))  # 👈 Will print the real error
        return jsonify({"reply": "No reply received or error!"}), 500
