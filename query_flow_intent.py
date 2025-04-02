# Toy example: Intent deduction with a "path of least resistance" vibe
class SimpleGrok:
    def __init__(self):
        # Fake "memory" of past convo
        self.context = []
        # Word weights to hint at intent (super basic)
        self.intent_clues = {
            "how": "process",
            "why": "reason",
            "what": "info",
            "vibe": "feel"
        }

    def analyze_query(self, query):
        # Split query into words
        words = query.lower().split()
        intent_score = {}
        
        # Look for intent clues
        for word in words:
            if word in self.intent_clues:
                intent = self.intent_clues[word]
                intent_score[intent] = intent_score.get(intent, 0) + 1
        
        # Pick the "easiest" path based on strongest clue
        if intent_score:
            guessed_intent = max(intent_score, key=intent_score.get)
        else:
            guessed_intent = "info"  # Default if no clear cue
        
        # Adjust based on context (if any)
        if self.context and "process" in self.context[-1]:
            guessed_intent = "process" if "how" in words else guessed_intent
        
        return guessed_intent

    def respond(self, query):
        intent = self.analyze_query(query)
        self.context.append(query)  # Update "memory"
        
        # Flow into a response based on intent
        if intent == "process":
            return "Here’s a step-by-step breakdown..."
        elif intent == "reason":
            return "Let me explain why that happens..."
        elif intent == "feel":
            return "It’s like a gut sense of..."
        else:
            return "Here’s some info on that..."
        
# Test it out
grok = SimpleGrok()
print(grok.respond("how does it work"))  # Process vibe
print(grok.respond("what’s the vibe"))  # Feel vibe
print(grok.respond("why is it like that"))  # Reason vibe
print(grok.respond("cool stuff"))  # Default info vibe



