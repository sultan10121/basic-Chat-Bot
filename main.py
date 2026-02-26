import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client()

# Store conversation history
conversation_history = []

def chat_with_gemini(user_input):
    try:
        conversation_history.append({"role": "user", "content": user_input})

        # Build conversation prompt
        full_prompt = ""
        for msg in conversation_history:
            full_prompt += f"{msg['role']}: {msg['content']}\n"

        # Generate response
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        reply = response.text.strip()

        conversation_history.append({"role": "assistant", "content": reply})

        return reply

    except Exception as e:
        return f"Error: {e}"
