from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import traceback  # For logging errors

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()  # Use safer method for JSON handling
        api_key = data.get("api_key")  
        user_message = data.get("message", "")

        if not api_key:
            return jsonify({"response": "Error: No API key provided."}), 400

        openai.api_key = api_key  # Set API key dynamically

        # Correct method call for OpenAI API
        response = openai.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:ramprasad-group:90-10f1:A3SX7B9n",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_message}]
        )

        bot_response = response.choices[0].message.content
        return jsonify({"response": bot_response})

    except openai.error.OpenAIError as e:  # Correct exception handling
        return jsonify({"response": f"OpenAI API error: {str(e)}"}), 500

    except Exception as e:
        traceback.print_exc()  # Print detailed error logs
        return jsonify({"response": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
