# M12 Ollama (Local AI)

## The "Why?"

Artificial Intelligence (AI) is no longer restricted to giant tech companies or paid subscriptions. With tools like **Ollama**, you can run powerful Large Language Models (LLMs)—similar to ChatGPT—directly on your own computer. This gives you total privacy (no data leaves your machine), works offline, and is completely free to use. By connecting Python to Ollama, you can build AI-powered apps that can summarize text, translate languages, or even generate code without needing an internet connection.

## Goals

Learn how to interact with the Ollama local API using Python, send prompts to an AI model, and process the AI-generated responses for use in your applications.

## Core Concepts

### Local LLMs
Large Language Models like **Llama 3**, **Mistral**, or **Gemma** are the "brains" of the AI. Ollama makes it easy to download and run these models on your local hardware.

### API Interaction
Ollama runs a local web server (usually on port 11434). Python can send a "prompt" (a question or instruction) to this server and wait for the AI to "generate" an answer.

### JSON Requests
To talk to Ollama, we send a JSON object containing the `model` name and the `prompt` text. The AI will then return its answer in another JSON object.

## Guided Practice

We will build a **Text Summarizer**. You will provide a paragraph of text, and the local AI will condense it into a single, punchy sentence.

*   **Step 1: Install Ollama and a model**
    Go to [ollama.com](https://ollama.com/) and install the software. Then run this in your terminal to download a small, fast model:
    ```bash
    ollama pull llama3
    ```

*   **Step 2: Create `ai_summarizer_example.py`**
    (Ensure you have the `requests` library installed from M09)
    ```python
    import requests
    import json

    def get_ai_response(prompt):
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False # We want the full answer at once
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                # The response is a JSON string; extract the 'response' field
                return response.json()['response']
            else:
                return f"Error: Ollama returned status {response.status_code}"
        except Exception as e:
            return f"Error: Could not connect to Ollama. Is it running? ({e})"

    # The text we want the AI to process
    long_text = """
    Python is a high-level, interpreted, general-purpose programming language. 
    Its design philosophy emphasizes code readability with the use of significant indentation. 
    Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, 
    including structured, object-oriented and functional programming.
    """

    print("AI is processing your text...")
    summary = get_ai_response(f"Summarize this in one short sentence: {long_text}")

    print("\n--- Summary ---")
    print(summary.strip())
    ```

## Checkpoints

* [ ] **The Professional Re-writer**:
    Modify the prompt to take a "rude" or "messy" email and rewrite it to be "extremely polite and professional."
* [ ] **AI Quiz Master**:
    Create a script where the user enters a topic (e.g., "Cats"), and the AI generates 3 multiple-choice questions about that topic.
* [ ] **Endless AI Chat**:
    Wrap the AI logic in a `while True` loop so you can have a continuous conversation with the model in your terminal. Use `input()` to get your message.