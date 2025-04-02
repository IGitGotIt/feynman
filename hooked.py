import streamlit as st
import requests
import time

# API setup (similar to martian.py)
API_KEY = "xai-D53FuQZlBWEk9u2BJl1VF2bK5BHmkalAirzMotUb03P45MdhJ65mjbwIt581LsbfGbvAVLSONebyLvkx"
API_URL = "https://api.x.ai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def call_grok_api(prompt, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": "grok-2-1212",
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.7
    }
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: API call failed ({response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize session state variables
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "round_number" not in st.session_state:
    st.session_state.round_number = 1
if "votes_a" not in st.session_state:
    st.session_state.votes_a = 0
if "votes_b" not in st.session_state:
    st.session_state.votes_b = 0
if "current_votes" not in st.session_state:
    st.session_state.current_votes = {}

# Streamlit setup
st.title("HookedHelloWorld: AI Banter")

# Trigger: Welcome message to pull users in
if not st.session_state.chat_started:
    st.write("Trigger: Two AIs are ready to spar—click to see who wins!")

# Action: Button to start/continue chat
start_button = st.button("Start New Chat" if not st.session_state.chat_started else "Continue Chat")

if start_button:
    if not st.session_state.chat_started:
        st.session_state.chat_history = []
        st.session_state.round_number = 1
        st.session_state.votes_a = 0
        st.session_state.votes_b = 0
        st.session_state.current_votes = {}
    st.session_state.chat_started = True

# Variable Reward: Agents chat with unpredictable replies
if st.session_state.chat_started:
    # Display round number and scores
    st.subheader(f"Round {st.session_state.round_number}")
    st.write(f"Current Scores - Agent A: {st.session_state.votes_a} | Agent B: {st.session_state.votes_b}")
    
    topics = [
        "Say something snarky about the weather",
        "Make a witty observation about technology",
        "Share a clever thought about modern life",
        "Give a sharp take on social media",
        "Make a smart remark about current trends"
    ]
    
    # Agent A's turn
    topic = topics[st.session_state.round_number % len(topics)]
    response_a = call_grok_api(topic, system="You're Agent A, witty and sharp.")
    st.write("Agent A:", response_a)
    
    # Small delay for better UX
    time.sleep(1)
    
    # Agent B's turn
    response_b = call_grok_api(
        f"Reply casually but cleverly to: '{response_a}'",
        system="You're Agent B, chill and laid-back but smart."
    )
    st.write("Agent B:", response_b)
    
    # Add responses to history
    st.session_state.chat_history.extend([
        f"Agent A: {response_a}",
        f"Agent B: {response_b}"
    ])
    
    # Create unique keys for this round's votes
    vote_key_a = f"vote_a_{st.session_state.round_number}"
    vote_key_b = f"vote_b_{st.session_state.round_number}"
    
    # Initialize vote tracking for this round if not exists
    if st.session_state.round_number not in st.session_state.current_votes:
        st.session_state.current_votes[st.session_state.round_number] = {"a": False, "b": False}
    
    # Voting system
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Vote for Agent A", key=vote_key_a):
            if not st.session_state.current_votes[st.session_state.round_number]["a"]:
                st.session_state.votes_a += 1
                st.session_state.current_votes[st.session_state.round_number]["a"] = True
                st.rerun()
    
    with col2:
        if st.button("Vote for Agent B", key=vote_key_b):
            if not st.session_state.current_votes[st.session_state.round_number]["b"]:
                st.session_state.votes_b += 1
                st.session_state.current_votes[st.session_state.round_number]["b"] = True
                st.rerun()
    
    # Display chat history
    st.subheader("Chat History")
    for msg in st.session_state.chat_history:
        st.write(msg)
    
    # Auto-increment round number
    if st.button("Next Round"):
        st.session_state.round_number += 1
        st.rerun()

# Add a reset button
if st.button("Reset Chat"):
    st.session_state.chat_started = False
    st.session_state.chat_history = []
    st.session_state.round_number = 1
    st.session_state.votes_a = 0
    st.session_state.votes_b = 0
    st.session_state.current_votes = {}
    st.rerun()
