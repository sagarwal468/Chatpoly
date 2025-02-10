from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    api_key = data.get("api_key")  # Get the user's OpenAI API key
    user_message = data.get("message", "")

    if not api_key:
        return jsonify({"response": "Error: No API key provided."}), 400

    try:
        # Use the provided API key to call OpenAI
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0125:ramprasad-group:90-10f1:A3SX7B9n",  # Replace with your fine-tuned model name
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_message}]
        )

        bot_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_response})

    except openai.error.OpenAIError as e:
        return jsonify({"response": f"OpenAI API error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
