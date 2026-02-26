import streamlit as st
from main import chat_with_gemini

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

st.title("🤖 Bot Instead of Friends")

# Store messages in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
if prompt := st.chat_input("Type your message..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from backend
    reply = chat_with_gemini(prompt)

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)