import streamlit as st
import requests
import time
import random

# API setup (similar to martian.py)
API_KEY = "xai-D53FuQZlBWEk9u2BJl1VF2bK5BHmkalAirzMotUb03P45MdhJ65mjbwIt581LsbfGbvAVLSONebyLvkx"
API_URL = "https://api.x.ai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def get_random_hook():
    hooks = [
        "🔥 Two AI titans are ready to throw down...",
        "⚡ Watch these bots roast each other into oblivion!",
        "🎭 Who's got more sass? You decide!",
        "🌟 Witness AI comedy evolve in real-time!",
        "🎪 Step right up to the greatest AI showdown!",
        "🎯 Every vote makes them sassier - how far will they go?",
        "🚀 Transform these AIs from mild to wild!",
        "💫 Create chaos, crown champions, cause comedy!",
        "🎨 Paint with personality - make these AIs legendary!",
        "🔮 Shape the future of AI sass!"
    ]
    return random.choice(hooks)

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
if "sass_level_a" not in st.session_state:
    st.session_state.sass_level_a = 1
if "sass_level_b" not in st.session_state:
    st.session_state.sass_level_b = 1
if "last_winner" not in st.session_state:
    st.session_state.last_winner = None

# Streamlit setup
st.title("HookedHelloWorld: AI Banter")

def get_agent_name(agent, sass_level):
    base_names = {
        'A': ["Witty Wanderer", "Sass Master", "Snark Lord", "Roast Champion", "Burn King"],
        'B': ["Chill Charmer", "Cool Cat", "Vibe Master", "Zen Zinger", "Flow Phoenix"]
    }
    level_idx = min(sass_level - 1, len(base_names[agent]) - 1)
    return base_names[agent][level_idx]

def get_system_prompt(agent, sass_level):
    base_prompt = "You're Agent {}, {}. "
    sass_multiplier = f"Your sassiness level is {sass_level}x normal - be {sass_level}x more clever and sharp in your responses."
    
    if agent == 'A':
        personality = "witty and sharp"
    else:
        personality = "chill and laid-back but smart"
    
    return base_prompt.format(agent, personality) + sass_multiplier

# Trigger: Welcome message to pull users in
if not st.session_state.chat_started:
    # Create a visually appealing container
    with st.container():
        st.markdown(f"### {get_random_hook()}")
        
        # Add some teasing preview text
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🤖 **Agent A** starts as *Witty Wanderer*")
        with col2:
            st.markdown("🤖 **Agent B** starts as *Chill Charmer*")
        
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h4>Who will reach legendary status first?</h4>
            <p>Each vote increases their sass level...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Make the start button more prominent
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🎮 START THE SHOWDOWN! 🎮", 
                        key="start_button",
                        help="Click to begin the AI sass battle!",
                        type="primary"):
                st.session_state.chat_started = True
                st.rerun()
else:
    # For continuing chat, make it less prominent but still engaging
    if st.button("🔄 Continue the Sass Battle!", 
                key="continue_button",
                help="Keep the banter going!"):
        st.rerun()

# Add this right after the chat starts to show progression potential
if st.session_state.chat_started and st.session_state.round_number == 1:
    st.markdown("""
    <div style='font-size: 0.8em; color: #888; text-align: center; padding: 10px;'>
        Progression Path:<br>
        Agent A: Witty Wanderer → Sass Master → Snark Lord → Roast Champion → Burn King<br>
        Agent B: Chill Charmer → Cool Cat → Vibe Master → Zen Zinger → Flow Phoenix
    </div>
    """, unsafe_allow_html=True)

# Variable Reward: Agents chat with unpredictable replies
if st.session_state.chat_started:
    # Display round number, scores, and current sass levels
    st.subheader(f"Round {st.session_state.round_number}")
    st.write(f"Current Scores - {get_agent_name('A', st.session_state.sass_level_a)}: {st.session_state.votes_a} | {get_agent_name('B', st.session_state.sass_level_b)}: {st.session_state.votes_b}")
    
    topics = [
        "Say something snarky about the weather",
        "Make a witty observation about technology",
        "Share a clever thought about modern life",
        "Give a sharp take on social media",
        "Make a smart remark about current trends"
    ]
    
    # Agent A's turn
    topic = topics[st.session_state.round_number % len(topics)]
    response_a = call_grok_api(topic, system=get_system_prompt('A', st.session_state.sass_level_a))
    st.write(f"{get_agent_name('A', st.session_state.sass_level_a)}:", response_a)
    
    # Small delay for better UX
    time.sleep(1)
    
    # Agent B's turn
    response_b = call_grok_api(
        f"Reply casually but cleverly to: '{response_a}'",
        system=get_system_prompt('B', st.session_state.sass_level_b)
    )
    st.write(f"{get_agent_name('B', st.session_state.sass_level_b)}:", response_b)
    
    # Add responses to history
    st.session_state.chat_history.extend([
        f"{get_agent_name('A', st.session_state.sass_level_a)}: {response_a}",
        f"{get_agent_name('B', st.session_state.sass_level_b)}: {response_b}"
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
        if st.button(f"Vote for {get_agent_name('A', st.session_state.sass_level_a)}", key=vote_key_a):
            if not st.session_state.current_votes[st.session_state.round_number]["a"]:
                st.session_state.votes_a += 1
                st.session_state.current_votes[st.session_state.round_number]["a"] = True
                st.session_state.sass_level_a += 1
                st.session_state.last_winner = 'A'
                st.rerun()
    
    with col2:
        if st.button(f"Vote for {get_agent_name('B', st.session_state.sass_level_b)}", key=vote_key_b):
            if not st.session_state.current_votes[st.session_state.round_number]["b"]:
                st.session_state.votes_b += 1
                st.session_state.current_votes[st.session_state.round_number]["b"] = True
                st.session_state.sass_level_b += 1
                st.session_state.last_winner = 'B'
                st.rerun()
    
    # Display last winner's sass increase
    if st.session_state.last_winner:
        st.write(f"🔥 {get_agent_name(st.session_state.last_winner, st.session_state['sass_level_' + st.session_state.last_winner.lower()])} is getting sassier!")
    
    # Display chat history
    st.subheader("Chat History")
    for msg in st.session_state.chat_history:
        st.write(msg)
    
    # Auto-increment round number
    if st.button("Next Round"):
        st.session_state.round_number += 1
        st.session_state.last_winner = None
        st.rerun()

# Add a reset button
if st.button("Reset Chat"):
    st.session_state.chat_started = False
    st.session_state.chat_history = []
    st.session_state.round_number = 1
    st.session_state.votes_a = 0
    st.session_state.votes_b = 0
    st.session_state.current_votes = {}
    st.session_state.sass_level_a = 1
    st.session_state.sass_level_b = 1
    st.session_state.last_winner = None
    st.rerun()
