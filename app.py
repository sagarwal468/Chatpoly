import streamlit as st
import requests

# Backend API URL (Ensure Flask is running)
BACKEND_URL = "http://127.0.0.1:5000/api/chat"

# Page Title
st.title("SmartPoly - Your Polymer Chat Assistant")

# Note about the chatbot
st.info("This chatbot is designed for polymer solubility predictions.")

# Example prompt
example_prompt = "Example: Is the polymer with SMILES [*]CCC(=O)O[*] soluble in TOL?"

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.write("### Chat History")
chat_container = st.container()
for msg in st.session_state.messages:
    sender, text = msg
    with chat_container:
        if sender == "user":
            st.chat_message("user").markdown(f"**You:** {text}")
        else:
            st.chat_message("assistant").markdown(f"**SmartPoly:** {text}")

# User input field
user_input = st.text_input("Type your message here", key="input")

# Send button functionality
if st.button("Send") and user_input.strip():
    # Append user message
    st.session_state.messages.append(("user", user_input))

    # Send request to backend
    response = requests.post(BACKEND_URL, json={"message": user_input})

    # Handle response
    if response.status_code == 200:
        bot_reply = response.json().get("response", "Error: No response from server")
        st.session_state.messages.append(("assistant", bot_reply))
        st.experimental_rerun()
    else:
        st.error("Failed to get response. Check API key and server status.")

# Display example prompt
st.markdown(f"_{example_prompt}_")
