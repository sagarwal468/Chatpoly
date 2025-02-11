from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        api_key = data.get("api_key")  
        user_message = data.get("message", "")

        if not api_key:
            return jsonify({"response": "Error: No API key provided."}), 400

        openai.api_key = api_key
        response = openai.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:ramprasad-group:90-10f1:A3SX7B9n",  
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_message}]
        )

        bot_response = response.choices[0].message.content
        return jsonify({"response": bot_response})

    except openai.OpenAIError as e:  # Fix: Correct way to catch OpenAI errors
        return jsonify({"response": f"OpenAI API error: {str(e)}"}), 500

    except Exception as e:  # General error handling
        import traceback
        traceback.print_exc()  # Print error in logs
        return jsonify({"response": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)  # Ensure it's accessible
