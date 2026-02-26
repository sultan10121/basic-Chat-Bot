import os
from dotenv import load_dotenv
from google import genai

# ---------------------------
# 1️⃣ Load API key from .env
# ---------------------------
load_dotenv()  # reads GENAI_API_KEY
client = genai.Client()  # auto uses GENAI_API_KEY

# ---------------------------
# 2️⃣ Conversation history
# ---------------------------
conversation_history = []

# ---------------------------
# 3️⃣ Function to chat with Gemini
# ---------------------------
def chat_gemini(user_input):
    try:
        # Add the user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Build a single prompt string from conversation
        full_prompt = ""
        for msg in conversation_history:
            full_prompt += f"{msg['role']}: {msg['content']}\n"

        # ---------------------------
        # 4️⃣ Call Gemini model
        # ---------------------------
        # You can pass full_prompt directly or as [{"text": full_prompt}]
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"text": full_prompt}]
        )

        # ---------------------------
        # 5️⃣ Access the reply text safely
        # ---------------------------
        bot_reply = response.text.strip()

        # Save assistant reply to history
        conversation_history.append({"role": "assistant", "content": bot_reply})

        return bot_reply

    except Exception as e:
        return f"Error: {e}"

# ---------------------------
# 6️⃣ Chat loop
# ---------------------------
print("Gemini Chatbot (type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    reply = chat_gemini(user_input)
    print("Chatbot:", reply)
