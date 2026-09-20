
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load .env
load_dotenv()

# Get OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

print("API key loaded:", bool(api_key))

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY not found in .env"
    )

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key.strip()
)

# Flask
app = Flask(__name__)


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return send_from_directory("website", "index.html")


# =========================
# AI CHAT
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "answer": "Please enter a message."
            })

        print("User:", user_message)

        # Ask MECORA
        response = client.chat.completions.create(

            model="openrouter/free",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are MECORA, an intelligent AI assistant "
                        "created by Ahmed Bendag, a Mechatronics Engineering Student. "
                        "Be helpful, friendly, clear and accurate."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        answer = response.choices[0].message.content

        print("MECORA:", answer)

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        # IMPORTANT:
        # Show the real error in the terminal
        print()
        print("========== MECORA ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        print("==================================")
        print()

        return jsonify({
            "answer": "MECORA encountered an error. Check the terminal."
        }), 500


# =========================
# START MECORA
# =========================

if __name__ == "__main__":

    print()
    print("================================")
    print("          🤖 MECORA")
    print("================================")
    print("Founded by Ahmed Bendag")
    print("Mechatronics Engineering Student")
    print()
    print("MECORA is starting...")
    print("Open: http://127.0.0.1:5000")
    print()

port = int(os.environ.get("PORT", 5000))
app.run(
    host="0.0.0.0",
    port=port,
    debug=False
)