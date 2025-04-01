import requests
import re

# Hypothetical xAI Grok API setup
API_KEY = "xai-D53FuQZlBWEk9u2BJl1VF2bK5BHmkalAirzMotUb03P45MdhJ65mjbwIt581LsbfGbvAVLSONebyLvkx"
API_URL = "https://api.x.ai/v1/chat/completions"  # Adjust per actual docs
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Feynman Prompts based on "Why Feynman?" rationales
PROMPTS = {
    "domain_name": "You’re a playful problem-solver like Richard Feynman. Help me generate or validate a domain name with a scientific twist: guess a creative name, compute its consequences (market fit, catchiness), and compare to real-world signals (e.g., X trends). Query: {query}",
    "book_publishing": "Channel Feynman’s knack for explaining complex ideas simply. Assist with book publishing—suggest titles, taglines, or strategies that make concepts clear and compelling. Query: {query}",
    "idea_testing": "Embody Feynman’s scientific curiosity for iterative testing. Run a thought experiment on this idea, simulate outcomes, and score them against real-world signals (e.g., X or web data). Query: {query}",
    "conversation_memory": "Use Feynman’s teaching style—breaking down old ideas anew. Retrieve and augment past conversation insights to answer this query, pulling from our chat history. Query: {query}",
    "learning": "Explain this like Feynman—simplify without dumbing down, as a learning companion. Break it into plain speak or give me a ‘teach it back’ prompt. Query: {query}",
    "crowdsourcing": "Tap Feynman’s love of experimentation. Simulate or suggest a crowdsourcing approach (e.g., voting, X polls) to test this, using virtual or real feedback. Query: {query}",
    "strategy": "Think like Feynman analyzing systems (e.g., Challenger disaster). Plan a publishing strategy—steps, niches, predictions—based on trends and logic. Query: {query}"
}

# Query type detection (basic keyword matching)
def detect_query_type(query):
    query = query.lower()
    if "domain" in query or "name" in query:
        return "domain_name"
    elif "book" in query or "publish" in query or "title" in query:
        return "book_publishing"
    elif "idea" in query or "test" in query or "experiment" in query:
        return "idea_testing"
    elif "past" in query or "conversation" in query or "remember" in query:
        return "conversation_memory"
    elif "explain" in query or "learn" in query or "understand" in query:
        return "learning"
    elif "vote" in query or "crowd" in query or "poll" in query:
        return "crowdsourcing"
    elif "strategy" in query or "plan" in query or "launch" in query:
        return "strategy"
    else:
        return "idea_testing"  # Default to broad use case

# Call Grok API
def call_grok_api(prompt):
    payload = {
        "model": "grok-2-1212",  # Hypothetical model name
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: API call failed ({response.status_code})"

def validate_feynman_response(response):
    characteristics = {
        'simplicity': lambda x: len([w for w in x.split() if len(w) > 7]) / len(x.split()) < 0.2,
        'examples': lambda x: "for example" in x.lower() or "like" in x.lower(),
        'step_by_step': lambda x: any(marker in x.lower() for marker in ["first", "then", "finally", "step"]),
    }
    
    scores = {name: check(response) for name, check in characteristics.items()}
    return scores

# Feynman Bot main function
def feynman_bot(query):
    query_type = detect_query_type(query)
    selected_prompt = PROMPTS[query_type].format(query=query)
    response = call_grok_api(selected_prompt)
    
    # Add validation
    scores = validate_feynman_response(response)
    if not all(scores.values()):
        print(f"Warning: Response may not fully align with Feynman style: {scores}")
    
    intro = "Alright, let's tackle this Feynman-style—simple, curious, and sharp!\n"
    return intro + response

def run_test_queries():
    test_queries = [
        "Suggest a domain for a physics poetry book",
        "Help me with a book title about quantum truth",
        "Test this idea: a subscription book box",
        "What did we say about domains last time?",
        "Explain Walsch’s observer quote",
        "How would 1,000 people vote on TruthLens.com?",
        "Plan a book launch for a spiritual physics book"
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        print(feynman_bot(q))
        print("-" * 50)

if __name__ == "__main__":
    run_test_queries()
