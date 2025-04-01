from feynman import feynman_bot

def main():
    print("Feynman Bot - Ask me anything! (type 'quit' to exit)")
    while True:
        query = input("\nYour question: ")
        if query.lower() == 'quit':
            break
        response = feynman_bot(query)
        print("\n" + response)

if __name__ == "__main__":
    main()