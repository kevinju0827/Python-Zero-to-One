# M16 Local AI (Ollama)

![Module 16 of 17](https://img.shields.io/badge/Module-16_of_17-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![1.5 hours](https://img.shields.io/badge/Time-1.5_hours-60a5fa?style=flat-square)
![Prerequisites: M01–M15](https://img.shields.io/badge/Prerequisites-M01–M15-94a3b8?style=flat-square)

**Topics covered:** local LLMs · Ollama setup · calling the API with `requests` · streaming vs. non-streaming · prompt engineering · defensive error handling · integrating AI into automation pipelines

## The Why?

Throughout this course you have used cloud AI (Gemini, ChatGPT) as a collaborator. That works beautifully for learning. In real production work, three problems quickly surface:

- **Privacy:** pasting customer emails, medical records, or legal documents into a cloud service may violate laws or contracts.
- **Cost:** every API call costs money. A script classifying 100,000 support tickets per day adds up fast.
- **Reliability:** cloud APIs go down, change pricing, or deprecate the model your code depends on — sometimes overnight.

**Ollama** solves all three. It runs Large Language Models (Llama 3, Mistral, Gemma, Phi, and many others) entirely on your machine. The model file lives on your disk, inference happens on your CPU/GPU, and zero data leaves your machine. The cost is zero. The service cannot disappear because *you* are the service.

In this module, you will combine everything you learned about `requests` (M11) with a locally running AI to build the kind of small AI-powered tools that used to require an entire ML team.

---

## Core Concepts

### What Is an LLM, Really?

A Large Language Model is a program that, given some text, predicts what text is most likely to come next. That prediction is informed by hundreds of billions of words the model was trained on, so the "most likely continuation" of a prompt like:

> *"Summarize this email in one polite sentence: …"*

turns out to be a genuinely useful summary.

What matters for practical use:
- The model is a **function**: text in → text out.
- The same prompt may produce slightly different outputs each run — LLMs are non-deterministic.
- Output quality is largely determined by prompt quality.

---

### Installing Ollama

1. Download from **[ollama.com](https://ollama.com/)** and run the installer.
2. Pull a model (one-time download, a few GB):
   ```bash
   ollama pull llama3
   ```
3. Verify it works:
   ```bash
   ollama run llama3
   ```
   Type a question and press Enter. You should see the model responding.

Once installed, Ollama runs in the background as a local HTTP server at `http://localhost:11434` — the same kind of API you called in M11.

---

### Calling Ollama from Python

The key endpoint is `POST /api/generate`:

```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": "Explain recursion in one sentence.",
        "stream": False,   # Wait for the full response
    },
    timeout=120,           # Local models can be slow on modest hardware
)
response.raise_for_status()
print(response.json()["response"])
```

The key you almost always need is `"response"` — the model's text output.

---

### Streaming vs. Non-Streaming

| Mode | Behavior | Best for |
|------|----------|---------|
| `"stream": False` | Wait for full response, receive one JSON object | Scripts, batch jobs |
| `"stream": True` | Receive chunks as they are generated (word by word) | Interactive chat UIs |

For learning and automation scripts, use `stream: False` — simpler to handle.

---

### Prompt Engineering — Three Rules That Cover 80% of Cases

**1. Give the model a role:**

```
You are a professional customer-success specialist.
Rewrite the following email to be polite, warm, and concise.
```

**2. Be explicit about the output format:**

```
Return ONLY a JSON object in this exact shape, no extra commentary:
{"category": "...", "priority": "high|medium|low"}
```

**3. Provide an example (few-shot prompting):**

```
Classify the ticket as 'billing', 'technical', or 'other'.

Example:
Ticket: "My invoice shows the wrong amount."
Category: billing

Now classify:
Ticket: "{ticket_text}"
Category:
```

---

### Defensive Calls — When Ollama Is Not Running

```python
def ask_llm(prompt: str) -> str:
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        return "[Error] Cannot reach Ollama. Is it running?"
    except requests.exceptions.HTTPError as e:
        return f"[Error] HTTP {e.response.status_code}. Did you run `ollama pull llama3`?"
    except requests.exceptions.Timeout:
        return "[Error] Model timed out. Try a shorter prompt or a smaller model."
```

---

## Going Further

<details>
<summary>The Chat Endpoint (`/api/chat`)</summary>

For multi-turn conversations, use `/api/chat` instead of `/api/generate`:

```python
messages = [
    {"role": "system", "content": "You are a concise Python tutor."},
    {"role": "user",   "content": "What is a list comprehension?"},
]

resp = requests.post(
    "http://localhost:11434/api/chat",
    json={"model": "llama3", "messages": messages, "stream": False},
    timeout=120,
)
print(resp.json()["message"]["content"])
```

</details>

<details>
<summary>Structured JSON Output</summary>

When you need machine-readable output, force JSON in the prompt AND parse the result:

```python
import json

prompt = """Classify this ticket as exactly one of: billing, technical, other.
Return ONLY: {"category": "..."}
Ticket: "I can't log in after the password reset."""

raw = ask_llm(prompt)
try:
    result = json.loads(raw)
    print(result["category"])
except json.JSONDecodeError:
    print("Model did not return valid JSON:", raw)
```

</details>

<details>
<summary>Choosing a Model</summary>

| Model | Size | Good for |
|-------|------|---------|
| `llama3` | ~4 GB | General-purpose, good quality |
| `phi3` | ~2 GB | Faster on low-RAM machines |
| `mistral` | ~4 GB | Instruction following |
| `gemma2` | ~5 GB | Google's open model |

Start with `phi3` if your machine has less than 8 GB RAM.

</details>

<details>
<summary>Combining Modules in a Pipeline</summary>

The real power comes from chaining modules:
- **M15 (schedule):** run the pipeline on a timer
- **M11 (requests):** fetch data to process
- **M16 (Ollama):** classify or summarize each item
- **M12 (SQLite):** store the results

This is the architecture of a real data-enrichment pipeline.

</details>

---

## Guided Practice

We will build a **polite-email rewriter** — the kind of internal tool a customer-success team would use daily. It takes a blunt draft and returns a warmer, clearer version without any data leaving the machine.

**Scenario:** A colleague writes technically correct but cold emails. We want a tool that polishes the tone automatically.

### Step 1 — Write the prompt

Create `email_polisher_example.py`. The prompt defines the model's role and output format:

```python
SYSTEM_PROMPT = """You are an experienced customer-success specialist.
Rewrite the following email to be polite, warm, and professional.
Return ONLY the rewritten email body. No subject line. No commentary."""
```

### Step 2 — Build the rewrite function

```python
import requests

def polish_email(draft: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nOriginal email:\n{draft}"
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        return "[Error] Ollama is not running. Start it from the menu bar."
    except requests.exceptions.Timeout:
        return "[Error] Model took too long. Try a shorter email."
```

### Step 3 — Test with contrasting drafts

```python
drafts = [
    "Refund not possible. Ticket closed.",
    "Auth token expired. API rejected. Check logs and fix config.",
]

for draft in drafts:
    print("--- Original ---")
    print(draft)
    print("\n--- Polished ---")
    print(polish_email(draft))
    print()
```

### Step 4 — Compare the outputs

Run the script. Compare how the model changed tone while preserving meaning. Notice how the role instruction (`"customer-success specialist"`) and the format instruction (`"Return ONLY the rewritten email"`) guide the output. Try removing them and see how the output changes.

---

## Checkpoints

* [ ] **Customer Ticket Triage**
  Create a `tickets.txt` with at least 8 lines — one ticket subject per line, mixing billing problems, password resets, feature requests, and spam.
  For each line, use few-shot prompting to ask the LLM to classify it as: `billing`, `account`, `feature_request`, or `other`.
  Print a summary: `"Processed 8 tickets — billing: 3, account: 2, feature_request: 1, other: 2"`
  *(Hint: use `collections.Counter` to tally the categories.)*

* [ ] **Local Code Reviewer**
  Build a script that reads a Python file (path from `input()`).
  Send the file contents to the LLM with a prompt asking for the top 3 concrete improvements, referencing specific function names or line numbers.
  Print the review.
  Try it on your M10 or M12 script — evaluate whether the suggestions are useful.

* [ ] **Daily News Digest with Sentiment**
  Combine M11 + M12 + M15 + M16.
  Every morning on a schedule, fetch the top 5 headlines from `https://hn.algolia.com/api/v1/search?tags=front_page` (Hacker News, no key needed).
  For each headline, ask the local LLM to classify sentiment (`positive`, `negative`, `neutral`) and summarize in one sentence.
  Store results in a SQLite table `headlines(id, fetched_on, title, sentiment, summary)`.
  Print: `"Today's mood: 3 positive, 1 neutral, 1 negative."`
