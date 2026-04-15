import requests
import json

def get_ai_response(prompt):
    """Function to send a prompt to the local Ollama API."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False # Wait for the entire response to finish
    }
    
    try:
        # We use a POST request to send our prompt data to the AI
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            # The AI's answer is stored inside the 'response' key of the JSON object
            return response.json()['response']
        else:
            return f"Error: Ollama returned status code {response.status_code}"
    except Exception as e:
        return f"Error: Could not connect to Ollama server. Is it running? ({e})"

# Practical Example: Summarizing a long block of text
text_to_process = """
Python is a high-level, interpreted, general-purpose programming language. 
Its design philosophy emphasizes code readability with the use of significant indentation. 
Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, 
including structured, object-oriented and functional programming.
Python is often described as a 'batteries included' language due to its comprehensive standard library.
"""

print("--- AI Text Processor ---")
print("Communicating with local Llama 3 model...")

# Ask the AI to summarize
prompt = f"Summarize this text into one short, punchy sentence: {text_to_process}"
result = get_ai_response(prompt)

print("\n--- AI Summary ---")
print(result.strip())
