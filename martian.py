import requests

# Hypothetical xAI Grok API setup
API_KEY = "xai-D53FuQZlBWEk9u2BJl1VF2bK5BHmkalAirzMotUb03P45MdhJ65mjbwIt581LsbfGbvAVLSONebyLvkx"
API_URL = "https://api.x.ai/v1/chat/completions"  # Adjust per xAI docs
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Prompts inspired by Feynman's "Martian model" (outsider lens, detailed breakdown)
PROMPTS = {
    "ignorance_perspective": """
        Channel Richard Feynman  (FeynmanBot) Feynman’s Martian model—step back and see this like a curious Martian who knows nothing about it. Describe how this situation—[query]—would look to someone with zero context, in vivid, simple detail. Break it down step-by-step, imagining their confusion, wonder, or missteps, with the same depth as your prior answers. Keep it playful, clear, and thorough.
    """,
    "assumptions": """
        Use Feynman’s systematic curiosity. For this—[query]—list the assumptions, expectations, and foregone conclusions being taken for granted. Then, explore what happens if we strip them away—how does it shift? Dive deep, like before, with examples and consequences, keeping it sharp and engaging.
    """,
    "outsider_perspective": """
        Think like Feynman’s Martian, viewing this—[query]—from wild angles: a complete outsider, someone from another planet, country, historical period, and younger/older self. Paint each perspective with rich, detailed imagination, matching your earlier style—quirky, insightful, and full.
    """,
    "word_meaning": """
        Feynman-style: question the labels in this—[query]. For each term or label used, ask: do I really know what it means? Dig into its layers—surface, implied, and perceived—then test it against outside views, like you did before, with depth and a touch of fun.
    """,
    "interesting_alternatives": """
        With Feynman’s playful problem-solving, find what’s interesting in this—[query]. Highlight its quirks, hooks, or hidden gems, then suggest other ways it could be, with vivid alternatives. Match your prior detailed, creative flair.
    """
}

# Query type detection (based on your questions)
def detect_query_type(query):
    query = query.lower()
    if "if i knew nothing" in query or "know nothing" in query:
        return "ignorance_perspective"
    elif "assumptions" in query or "expectations" in query or "foregone" in query:
        return "assumptions"
    elif "outsider" in query or "different planet" in query or "historical" in query or "younger" in query:
        return "outsider_perspective"
    elif "term" in query or "label" in query or "means" in query:
        return "word_meaning"
    elif "interesting" in query or "some other way" in query:
        return "interesting_alternatives"
    else:
        return "ignorance_perspective"  # Default

# Call Grok API
def call_grok_api(prompt):
    payload = {
        "model": "grok-2-1212",  # Hypothetical model
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500  # More tokens for detailed answers
    }
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: API call failed ({response.status_code})"

# Feynman Bot main function
def feynman_bot(query):
    query_type = detect_query_type(query)
    print(f"Detected query type: {query_type}")
    
    # Insert query into prompt
    selected_prompt = PROMPTS[query_type].replace("[query]", query)
    
    # Call API and synthesize response
    response = call_grok_api(selected_prompt)
    intro = "Hey, let’s crack this open Feynman-style—like a Martian peering at Earth, curious and clear-headed!\n"
    return intro + response

# Test your questions
questions = [
    "What would bot-to-bot communication look like if I knew nothing about AI or language models? How would two artificial minds exchanging information appear to a complete outsider?",
    "What assumptions do we make about how AI assistants communicate with each other? What if we remove our human-centric communication paradigms?",
    "How might bot conversations look to different observers: to a classical computer scientist from the 1960s, to a modern AI researcher, to future AI systems? What patterns or behaviors would each notice?",
    "When we say 'bots are communicating', what does that actually mean? What's really happening at each layer of their interaction?",
    "What interesting emergent behaviors could arise from bot-to-bot communication? Could they develop unexpected patterns or protocols?"
]

def run_test_queries():
    q = questions[0]  # Get only the first question
    print(f"\nQuery: {q}")
    print(feynman_bot(q))
    print("-" * 50)

if __name__ == "__main__":
    run_test_queries()

