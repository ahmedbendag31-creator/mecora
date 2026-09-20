
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

print("API key loaded:", bool(api_key))

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

print("🤖 AI Agent started!")
print("Type 'quit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Agent stopped.")
        break

    response = client.chat.completions.create(
        model="openrouter/free",,
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("AI:", response.choices[0].message.content)