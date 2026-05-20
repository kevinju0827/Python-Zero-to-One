# M12 Ollama (Local AI)

## The "Why?"

Throughout this course, you have used cloud AI assistants like Gemini to generate code, explain concepts, and brainstorm. That works wonderfully for *learning*. But in real production work, three issues quickly surface:

* **Privacy**: Pasting customer emails, legal documents, or medical records into a cloud service may be illegal or a contract violation.
* **Cost**: Every API call costs money. A script that classifies 100,000 support tickets per day adds up fast.
* **Reliability**: Cloud APIs go down, change pricing, or deprecate the model your code depends on.

**Ollama** solves all three. It is a tool that runs Large Language Models (LLMs)—Llama 3, Mistral, Gemma, Phi, and many others—on *your own laptop*. The model file lives on your disk; the inference happens on your hardware; no data ever leaves the machine. The cost is zero. The service can never disappear because *you* are the service.

In this module, you will combine everything you have learned about `requests` (M09) with a locally running AI to build the kind of small AI-powered tools that, just a few years ago, required an entire team of ML engineers to deploy. The lesson here is bigger than syntax: once you can call a local model from Python, you can embed real "reasoning" into any automation you build.

## Goals

By the end of this module, you should be able to:

* Install Ollama on your machine and pull a model.
* Explain why running a model locally matters for privacy, cost, and reliability.
* Send a prompt to Ollama's local HTTP API using `requests`.
* Distinguish between streaming and non-streaming responses and choose the right one for your use case.
* Write effective prompts—giving the model a clear role, format, and example output.
* Handle the case where Ollama is not running or the model is not installed.
* Combine an LLM with other modules (`requests` + `sqlite3` + `schedule`) to build practical AI workflows.

## Core Concepts

### What is an LLM, Really?

A Large Language Model is a program that, given some text, predicts what text is most likely to come next. That sounds modest, but the prediction is informed by hundreds of billions of words of text the model has been trained on, so the "most likely continuation" of a prompt like *"Summarize the following email in one polite sentence: …"* turns out to be a genuinely useful summary.

You do not need to understand the math to use one effectively. What matters in practice is:

* The model is a **function** that takes a prompt (text in) and returns a completion (text out).
* The same prompt may return slightly different outputs each time—LLMs are non-deterministic by default.
* The quality of the output is largely controlled by the quality of the **prompt**.

---

### Ollama: A Local Model Runner

Ollama is the friendliest tool for running open-source LLMs on your own machine. Once installed, it runs quietly in the background as a local HTTP server—usually listening on `http://localhost:11434`—and exposes a simple JSON API. This means you talk to it the same way you talked to JSONPlaceholder in M09: `requests.post(url, json=payload)`.

**Install:**

1. Download from [ollama.com](https://ollama.com/) and run the installer.
2. From your terminal, pull a small model to start with:
   ```bash
   ollama pull llama3
   ```
   This downloads the model file (a few gigabytes) to your disk—a one-time cost. After that, the model works offline.

You can list installed models with `ollama list` and run a quick interactive chat with `ollama run llama3` to confirm everything works.

---

### Calling Ollama from Python

The endpoint you will use most often is `POST /api/generate`. The request body is a JSON object with two required fields—`model` and `prompt`—plus several optional ones.

```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": "Explain recursion in one sentence.",
        "stream": False,         # Wait for the full answer in one response
    },
    timeout=120,                 # Local models can take a while on small machines
)
response.raise_for_status()
print(response.json()["response"])
```

The reply is a JSON object; the key you almost always care about is `"response"`, which contains the model's text answer.

---

### Streaming vs. Non-Streaming

When `stream` is `False`, Ollama waits until the model has finished generating, then sends one large JSON response. Easy to handle, but the user sees nothing until the whole answer is ready.

When `stream` is `True`, Ollama sends a series of small JSON chunks as the model produces them—the same word-by-word effect you see in ChatGPT. This is great for interactive chat UIs, but harder to parse (you have to read the response line by line).

For learning scripts and one-shot jobs, non-streaming (`stream=False`) is simpler and recommended. Reach for streaming once you build interactive interfaces.

---

### Prompt Engineering: Talking to the Model Effectively

The single biggest factor in the quality of LLM output is your prompt. Three rules cover 80% of the wins:

**1. Give the model a role.**

Bad: `"Summarize this email."`
Better: `"You are a professional executive assistant. Rewrite the following email so it is polite, concise, and ready to send to a CEO."`

**2. Be explicit about the output format.**

If you need machine-readable output (so your script can `json.loads()` it), say so:

```
Return ONLY a JSON object in this exact shape, with no extra commentary:
{"category": "...", "priority": "high|medium|low"}
```

**3. Provide an example (few-shot prompting).**

Showing one or two examples of the input/output you want dramatically improves accuracy:

```
Classify the customer ticket below as 'billing', 'technical', or 'other'.

Example:
Ticket: "My invoice shows the wrong amount."
Category: billing

Now classify this ticket:
Ticket: "{user_ticket}"
Category:
```

---

### Defensive Calls: When Ollama Isn't Available

The script will fail in a few predictable ways: Ollama isn't running, the model name is typoed, or the network call times out. Wrap every call:

```python
def ask(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        return "[Error] Cannot reach Ollama. Is it running? Start it from your menu bar."
    except requests.exceptions.HTTPError as e:
        return f"[Error] Ollama returned {e.response.status_code}. Did you `ollama pull` the model?"
    except requests.exceptions.Timeout:
        return "[Error] The model took too long. Try a smaller model or a shorter prompt."
```

This is the same defensive pattern you learned in M09—you are now applying it to a new kind of service.

---

## Guided Practice

We will build a **polite-email rewriter**—the kind of internal tool a real customer-success team would happily pay for, but you can build in 20 lines. The script feeds a blunt draft to your local LLM and returns a warmer, clearer version while preserving the original meaning.

**Scenario**: A colleague writes technically correct but cold emails to customers. We want a tool that takes the rough draft in and returns a polished version, all without any data ever leaving the laptop.

**Step 1: Write a prompt that gives the model a role and a clear format.** Tell the model it is *"an experienced customer-success specialist,"* ask it to rewrite the email to be *"polite, warm, and clear,"* and—critically—tell it to return ONLY the rewritten body with no commentary or headers. Vague prompts give vague results.

**Step 2: Send the prompt to Ollama's local API.** Use `requests.post("http://localhost:11434/api/generate", json={...}, timeout=120)`. Set `"stream": False` so you get one complete response instead of a stream of partial chunks.

**Step 3: Wrap the call in defensive `try/except` blocks.** Three failure modes happen in practice:
* `ConnectionError` — Ollama isn't running.
* `HTTPError` — the model name was typoed or hasn't been pulled.
* `Timeout` — your machine is slow or the prompt is too long.

Each one deserves a clear error message that tells the user how to fix it, not a stack trace.

**Step 4: Try it on two contrasting drafts.** Run the script with one short and abrupt draft (`"Refund not possible. Closing ticket."`) and one overly technical one (`"Your auth token expired so the API rejected the request..."`). Compare the model's outputs—you will see how prompt + role together change the tone.

The full implementation is in `email_polisher_example.py`. Make sure Ollama is running (`ollama run llama3` in a separate terminal) before you execute the script.

---

## Checkpoints

* [ ] **Customer Ticket Triage**:
      You volunteer to help a small nonprofit that receives 30–50 support emails a day. Build a script that:
      1. Reads a file `tickets.txt` where each line is one ticket subject (write at least eight realistic examples spanning billing problems, password resets, feature requests, and unrelated spam).
      2. For each line, asks the LLM to classify it as exactly one of: `billing`, `account`, `feature_request`, or `other`. Use few-shot prompting (include 2–3 examples in the prompt) to improve accuracy.
      3. Prints a summary like `"Processed 12 tickets — billing: 4, account: 3, feature_request: 2, other: 3"`.
      *(Hint: store each classification in a Python `Counter` from the `collections` module. This is the kind of automation that, in a real company, would replace hours of manual triage every week.)*

* [ ] **Local AI Code Reviewer**:
      Build a script that reads a Python file (path passed via `input()`), sends the entire contents to the LLM with the prompt *"You are a senior Python reviewer. List the top 3 concrete improvements you would suggest for the code below. Use plain bullet points. Be specific—reference function names or line numbers when possible."*, and prints the review.
      Try it on one of your own scripts from an earlier module (e.g., your M08 sales calculator or your M10 expense tracker). The point of this checkpoint is not to get a perfect review—it is to get used to integrating an LLM as a *co-developer in your toolchain* without leaking your code to a cloud provider.

* [ ] **Daily News Digest with Sentiment**:
      Combine M09 + M10 + M11 + M12. Build a small automation that:
      1. Every morning at a set time (use `schedule`), fetches the top 5 headlines from a free news API such as `https://hn.algolia.com/api/v1/search?tags=front_page` (Hacker News, no key needed).
      2. For each headline, asks the local LLM to classify its overall sentiment as `positive`, `negative`, or `neutral` and to summarize the headline in one sentence.
      3. Writes the results into a SQLite table `headlines(id, fetched_on, title, sentiment, summary)`.
      4. Prints a one-line report each morning: `"Today's mood: 3 positive, 1 neutral, 1 negative."`
      *(Hint: for testing, switch the schedule to every 60 seconds. Once you confirm the full pipeline works end-to-end, set it back to the real daily time. This single script integrates four modules' worth of skills—when you finish it, you have built a small but genuine production-style data pipeline.)*
