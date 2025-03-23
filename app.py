import streamlit as st
from nlp_parser import parse_input
from agent import BookingAgent

st.set_page_config(page_title="Hotel Booking Agent", page_icon="🛎️")
st.title("🛎️ AI Hotel Booking Chatbot")

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = BookingAgent()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Chat input from user
user_input = st.text_input("You:", key="input")

if user_input:
    agent = st.session_state.agent

    if agent.awaiting_confirmation:
        bot_response = agent.finalize_booking(user_input)
    else:
        intent, slots = parse_input(user_input)
        bot_response = agent.handle_intent(intent, slots)

    # Update chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Agent", bot_response))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**🛎️ Agent:** {message}")

st.markdown("---")
st.caption("Type 'exit' or 'quit' to end session.")
