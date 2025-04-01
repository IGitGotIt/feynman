from feynman import feynman_bot
from martian import feynman_bot as martian_bot

def main():
    print("Feynman Bot - Ask me anything! (type 'quit' to exit)")
    while True:
        query = input("\nYour question: ")
        if query.lower() == 'quit':
            break
        response = feynman_bot(query)
        print("\n" + response)

def bot_conversation():
    print("\n=== Starting Bot Conversation ===\n")
    
    initial_topic = "What is consciousness and how do artificial minds experience it?"
    conversation_history = ""
    
    print(f"Initial Topic: {initial_topic}\n")
    
    for round in range(3):
        print(f"\n--- Round {round + 1} ---\n")
        
        # Feynman bot considers the history and responds
        feynman_prompt = initial_topic if round == 0 else f"Given our previous discussion: {conversation_history}\nHow would you further develop or challenge these ideas about consciousness?"
        feynman_response = feynman_bot(feynman_prompt)
        print("Feynman Bot:", feynman_response)
        
        # Update conversation history
        conversation_history += f"\nFeynman: {feynman_response}"
        
        # Martian bot analyzes with context
        martian_prompt = f"Analyzing the ongoing discussion about consciousness: {conversation_history}\nWhat new patterns or assumptions do you notice from an outsider's perspective?"
        martian_response = martian_bot(martian_prompt)
        print("\nMartian Bot:", martian_response)
        
        # Update conversation history
        conversation_history += f"\nMartian: {martian_response}"
        
        print("\n" + "-"*50)

if __name__ == "__main__":
    print("Welcome to the Bot Conversation System!")
    print("1: Regular chat with Feynman Bot")
    print("2: Watch Feynman and Martian Bots converse")
    
    while True:
        mode = input("\nChoose mode (1 or 2): ").strip()
        if mode in ["1", "2"]:
            break
        print("Please enter either 1 or 2")
    
    if mode == "2":
        bot_conversation()
    else:
        main()
