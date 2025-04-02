import requests
import pyperclip
import time

# Hypothetical xAI Grok API setup
API_KEY = "xai-D53FuQZlBWEk9u2BJl1VF2bK5BHmkalAirzMotUb03P45MdhJ65mjbwIt581LsbfGbvAVLSONebyLvkx"
API_URL = "https://api.x.ai/v1/chat/completions"  # Adjust per xAI docs
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


# Call Grok API
def call_grok_api(prompt):
    payload = {
        "model": "grok-2-1212",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    try:
        print(".", end="", flush=True)  # Progress indicator
        # Add timeout of 10 seconds
        response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"\nAPI Error: Status {response.status_code}")
            return f"Error: API call failed ({response.status_code})"
    except requests.exceptions.Timeout:
        print("\nTimeout: API call took too long")
        return "Error: API timeout"
    except requests.exceptions.RequestException as e:
        print(f"\nNetwork Error: {str(e)}")
        return f"Error: Network issue"
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        return f"Error: {str(e)}"

def five_whys(initial_response):
    whys = []
    current_prompt = initial_response
    
    print("\nAnalyzing with 5 Whys:")
    for i in range(5):
        print(f"\nProcessing Why #{i+1}", end="")
        
        # Different prompts for each level to force deeper analysis
        if i == 0:
            why_prompt = f"What is the fundamental reason behind this approach? Focus on the core motivation: '{current_prompt}'"
        elif i == 1:
            why_prompt = f"Looking deeper, what underlying assumptions or beliefs drive this motivation? '{current_prompt}'"
        elif i == 2:
            why_prompt = f"What basic human or societal need does this address? Strip away all technology and process - what's at the core? '{current_prompt}'"
        elif i == 3:
            why_prompt = f"What primal or evolutionary factor might explain this need? Go beyond current context: '{current_prompt}'"
        else:
            why_prompt = f"What is the most fundamental truth or principle at play here? Reach for the absolute root: '{current_prompt}'"
        
        why_response = call_grok_api(why_prompt)
        
        if why_response.startswith("Error:"):
            print(f"\nStopping analysis due to error at Why #{i+1}")
            break
            
        whys.append(f"Why #{i+1}: {why_response}")
        print(f"\nResponse #{i+1}: {why_response}")
        current_prompt = why_response
        time.sleep(1)
    
    return "\n\n".join(whys) if whys else "Analysis could not be completed due to API errors"

if __name__ == "__main__":
    try:
        user_question = input("\nEnter your question: ")
        share_link = input("\nEnter share link (optional, press Enter to skip): ").strip()
        
        context = f" (Context: {share_link})" if share_link else ""
        martian_prompt = f"How might a martian look at '{user_question}'. Any context is provided here: '{context}'. Give the response in a paragraph"
        
        print("\nGetting initial response", end="")
        initial_response = call_grok_api(martian_prompt)
        
        if initial_response.startswith("Error:"):
            print("\nCould not get initial response. Please try again.")
        else:
            why_analysis = five_whys(initial_response)
            
            full_response = f"""
Initial Martian Response:
------------------------
{initial_response}

5 Whys Analysis:
---------------
{why_analysis}
"""
            
            print("\n\nFinal Response:")
            print(full_response)
            pyperclip.copy(full_response)
            print("\n(Full response copied to clipboard)")
            
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")

