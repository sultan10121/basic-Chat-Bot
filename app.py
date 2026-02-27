import streamlit as st
import whisper
import pyttsx3
import speech_recognition as sr
import threading
from main import chat_with_gemini

# ----------------------------
# Load Whisper Model
# ----------------------------
whisper_model = whisper.load_model("base")

# ----------------------------
# Text-to-Speech Engine
# ----------------------------
engine = pyttsx3.init()

def speak(text, mode):
    """Speak only if mode requires voice reply."""
    if mode in ["Text → Voice", "Voice → Voice"]:
        def run_speech():
            engine.say(text)
            engine.runAndWait()
        threading.Thread(target=run_speech, daemon=True).start()

# ----------------------------
# Voice Recording
# ----------------------------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)

    with open("voice.wav", "wb") as f:
        f.write(audio.get_wav_data())

    result = whisper_model.transcribe("voice.wav")
    return result["text"]

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini AI Chatbot (ChatGPT-style)")

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.header("Settings")

language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Urdu", "Spanish", "French", "German", "Arabic"]
)

mode = st.sidebar.radio(
    "Select Mode",
    ["Voice → Text", "Text → Voice", "Voice → Voice"]
)

# ----------------------------
# Conversation Memory
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# Voice Input Button
# ----------------------------
if st.button("🎤 Speak"):
    try:
        voice_text = listen()
    except Exception as e:
        st.error(f"Error accessing microphone: {e}")
        voice_text = ""

    if voice_text:
        st.session_state.messages.append({"role": "user", "content": voice_text})
        with st.chat_message("user"):
            st.markdown(voice_text)

        reply = chat_with_gemini(voice_text, language)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

        # Speak if mode requires
        speak(reply, mode)

# ----------------------------
# Text Input
# ----------------------------
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = chat_with_gemini(prompt, language)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Speak if mode requires
    speak(reply, mode)