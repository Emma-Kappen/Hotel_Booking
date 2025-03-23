import streamlit as st
from nlp_parser import parse_input
from agent import BookingAgent
from streamlit_chat import message
import speech_recognition as sr

st.set_page_config(page_title="Hotel Booking Chatbot", page_icon="🛎️")
st.title("🛎️ AI Hotel Booking Chatbot")

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = BookingAgent()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to process user message
def process_message(user_input):
    agent = st.session_state.agent

    if agent.awaiting_confirmation:
        bot_response = agent.finalize_booking(user_input)
    else:
        intent, slots = parse_input(user_input)
        bot_response = agent.handle_intent(intent, slots)

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", bot_response))

# Voice input option
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now!")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            st.success(f"You said: {text}")
            process_message(text)
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError:
            st.error("Voice recognition service unavailable.")

# Sidebar for voice input
st.sidebar.header("🎤 Voice Input")
if st.sidebar.button("Start Recording"):
    voice_input()

# Text input
user_input = st.text_input("Type your message here:", key="input")
if user_input:
    process_message(user_input)

# Display chat bubbles
for i, (sender, message_text) in enumerate(st.session_state.chat_history):
    is_user = sender == "user"
    message(message_text, is_user=is_user, key=str(i), avatar_style="adventurer" if is_user else "bottts")

# Footer
st.markdown("---")
st.caption("Type 'exit' or 'quit' to end session. Voice input uses your microphone.")
