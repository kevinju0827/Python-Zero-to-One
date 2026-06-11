# M16 Local AI (Ollama)

![Module 16 of 16](https://img.shields.io/badge/Module-16_of_16-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![2 hours](https://img.shields.io/badge/Time-2_hours-60a5fa?style=flat-square)
![Prerequisites: M11 — Web Requests](https://img.shields.io/badge/Prerequisites-M11:_Web_Requests-94a3b8?style=flat-square)

**Topics covered:** local LLMs · Ollama setup · the `ollama` library · messages & roles · system prompts · prompt engineering · `format="json"` structured output · `temperature` · streaming · defensive AI calls

## The Why?

This course began with a promise: use AI to help you write programs. This final module flips it around — **your programs use AI**.

Every program you have written so far computes with *structured* data: numbers, exact strings, rows, JSON keys. Show it a sentence like *"Waited twenty-five minutes for my food and the staff never even apologized"* and it is helpless — no `if` statement can tell you this customer is angry about service. A Large Language Model can. Plugging one into your code gives your programs a new ability: **reading messy human text** — classifying it, summarizing it, rewriting it, extracting data from it.

You could do this with a cloud API (ChatGPT, Gemini, Claude). But cloud AI has three problems for real work:

- **Privacy:** pasting customer emails or medical records into a cloud service may violate laws or contracts.
- **Cost:** every call costs money. Classifying 100,000 support tickets a day adds up fast.
- **Reliability:** cloud APIs go down, change pricing, or retire the model your code depends on — sometimes overnight.

**Ollama** removes all three. It runs open models (Qwen, Llama, Gemma, Mistral...) entirely on your machine: the model file lives on your disk, zero data leaves your computer, and the price is zero. You will combine it with M11's API skills and M10's CSV + JSON to build the kind of small AI-powered tool that used to require an ML team.

---

## Core Concepts

### What Is an LLM, Really?

A Large Language Model is a program that, given some text, predicts what text most likely comes next — informed by the billions of words it was trained on. The "most likely continuation" of *"Summarize this email in one sentence:"* turns out to be a genuinely useful summary.

What matters for using one in code:

- The model is a **function**: text in → text out. Nothing magical at the calling end.
- The same prompt can produce **different output each run** — LLMs are non-deterministic.
- It **predicts plausible text; it does not look up facts**. It will state wrong things confidently (a "hallucination"). Never treat its output as verified truth.
- Output quality is mostly determined by **prompt quality** — that is the skill you are training here.

---

### Installing Ollama and Pulling a Model

1. Download from **[ollama.com](https://ollama.com/)** and run the installer. Ollama then runs in the background.
2. Download a model (one-time, a few GB — do this on good Wi-Fi):

   ```bash
   ollama pull qwen2.5:7b
   ```

3. Smoke-test it in the terminal:

   ```bash
   ollama run qwen2.5:7b
   ```

   Type a question, get an answer, then exit with `/bye`.

**Why `qwen2.5:7b`?** It is a strong all-round small model that follows formatting instructions well — exactly what you need when code, not a human, reads the output. It needs roughly 8 GB of RAM. Alternatives:

| Model | Size | RAM | Notes |
|-------|------|-----|-------|
| `qwen2.5:7b` | ~4.7 GB | 8 GB+ | Best instruction-following of the three — course default |
| `qwen2.5:3b` | ~1.9 GB | 4 GB+ | Same family, lighter machines |
| `llama3.2:3b` | ~2 GB | 4 GB+ | Popular lightweight alternative |

Everything in this module works with any of them — change one string.

---

### Ollama Is a Server (You Have Built One of These)

When Ollama is running, it listens at `http://localhost:11434` — a REST API on your own machine, exactly the kind you *called* in M11 and *built* in M13:

```
your script  ──HTTP──▶  Ollama server (localhost:11434)  ──▶  model on your disk
     ◀──────────────────  generated text  ◀─────────────────────┘
```

Nothing new conceptually. The only difference from M11: this API speaks human language.

---

### First Call from Python

Install the official client:

```bash
pip install ollama
```

```python
import ollama

response = ollama.chat(
    model="qwen2.5:7b",
    messages=[
        {"role": "user", "content": "What is a variable in Python?"},
    ],
)
print(response["message"]["content"])
```

```
In Python, a variable is a name that refers to a value stored in memory.
Variables allow you to store data so that it can be manipulated and used
throughout your program. Here are some key points about variables in Python:

1. **Dynamic Typing**: Python is dynamically typed, meaning you don't need
   to declare the type of a variable when you create it. ...
```

...followed by roughly **forty more lines** of bullet points and code samples.

That is the entire core API. `messages` is a list of dictionaries (M04), the reply comes back as a dictionary, and the text lives at `["message"]["content"]`.

(Look closely at that output. You asked a simple question and got an essay. Hold that thought — the next section gives you the control panel.)

> **Under the hood** it is just M11: the library sends `requests.post("http://localhost:11434/api/chat", json={...})` for you. You could write this module with raw `requests` — the package only saves boilerplate. AI calls are API calls; there is no magic layer.

---

### Messages and Roles — How Conversations Work

Each message dictionary has a `role`:

| Role | Who is speaking | Used for |
|------|-----------------|---------|
| `system` | You, setting the rules | Personality, tone, language, output format — obeyed for the whole conversation |
| `user` | The human | Questions, input data |
| `assistant` | The model | Its previous replies |

The `system` message is your control panel. Left to its own devices the model fills every unstated gap with maximum helpfulness — that forty-line essay you just got. Set the rules once and they hold for the whole conversation:

```python
messages = [
    {"role": "system", "content": "You are a teaching assistant for absolute "
                                  "beginners. Always answer in one short "
                                  "sentence, with no code and no markdown."},
    {"role": "user",   "content": "What is a variable in Python?"},
]
```

```
A variable in Python is a name that refers to a value or object.
```

Same model, same question — one sentence instead of an essay. Every serious AI application you have used has a system prompt working behind the scenes like this.

Second key fact: **the model has no memory.** Every call starts from zero. A "conversation" is an illusion you maintain by resending the whole history each time:

```python
messages.append({"role": "assistant", "content": reply})                    # What it said
messages.append({"role": "user", "content": "Can you give an example?"})    # Your follow-up
response = ollama.chat(model="qwen2.5:7b", messages=messages)               # Send EVERYTHING again
```

The model only "remembers" what is inside the list you send. (This also explains why long chats get slow — the input keeps growing.)

---

### Prompt Engineering — The Four Building Blocks

A prompt that works once is luck; a prompt that works every time is engineering. Reliable prompts are assembled from four building blocks:

**1. Instruction — what to do.** The task itself, stated as one clear command. Verb first, specific, no ambiguity:

```
Classify the customer review below.
```

Weak instructions produce wandering answers. "Tell me about this review" invites an essay; "Classify the review" demands a verdict.

**2. Constraints — the rules of the answer.** Format, length, allowed values, what NOT to do. The model fills every unstated gap with chattiness ("Sure! Here is the classification you asked for..."), so if code will read the output, leave no room:

```
Return ONLY the category name. No explanation, no other text.
The category MUST be one of: food, service, environment, price.
```

**3. Context — what the model needs to know.** The background that shapes judgment: who the model is supposed to be (a role/persona), the situation, and the input data itself. Quality jumps when the model knows whose eyes to look through:

```
You are a cafe manager with ten years of experience, skilled at spotting
concrete, fixable problems in customer feedback.

Review: "{text}"
```

**4. Examples — show, don't just tell.** One worked example (called *few-shot prompting*) beats three sentences of description, especially for format or edge cases words struggle to pin down:

```
Example:
Review: "Great coffee but the barista was rude." → service
```

Assembled, the four blocks make one prompt:

```
You are a cafe manager reviewing customer feedback.            ← context (role)

Classify the review as: food, service, environment, or price.  ← instruction

Return ONLY the category name. No explanation.                 ← constraints

Example:                                                       ← examples
Review: "Great coffee but the barista was rude." → service

Review: "{text}" →                                             ← context (data)
```

Not every prompt needs all four — a simple task may skip the examples, a general question may skip constraints. But when a prompt misbehaves, debug it like code: check the blocks one at a time. *Is the instruction one clear task? Did a constraint get left unstated? Is context missing? Would one example settle it?*

---

### Structured Output — Turning Text into Data

The single most useful trick in this module. Free-text replies are for humans; **your program needs data**. Ask for JSON and pass `format="json"`, which forces Ollama to emit syntactically valid JSON:

```python
import json

prompt = """Analyze this review. Reply with ONLY JSON in this format:
{"sentiment": "positive|negative|neutral", "category": "food|service|environment|price"}

Review: "Waited twenty-five minutes for my food and the staff never even apologized.\""""

response = ollama.chat(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": prompt}],
    format="json",                  # Guarantee valid JSON syntax
    options={"temperature": 0},     # Classification wants consistency, not creativity
)
result = json.loads(response["message"]["content"])   # M10's json — full circle
print(result["sentiment"], result["category"])        # → negative service
```

Now the LLM is a normal function returning a dictionary — you can `if` on it, count it, store it in SQLite (M12), or chart it with M15's pandas. This pattern (LLM + JSON + loop) is the backbone of nearly every real-world "AI feature."

About `temperature`: it controls randomness. `0` = pick the most likely token every time (classification, extraction); higher (`0.7`–`1.0`, the default range) = varied, creative output (writing, brainstorming). One number, two different tools.

> `format="json"` guarantees *valid JSON syntax* — it does not guarantee the **keys or values** you asked for. The model can still return `{"feeling": "bad"}`. Spell out the exact shape in the prompt, and validate before trusting (next section).

---

### Defensive AI Calls — Three Ways It Fails

A local AI call has all of M08's failure modes plus one new one:

```python
import json
import ollama

def ask(prompt: str) -> dict:
    try:
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=[{"role": "user", "content": prompt}],
            format="json",
        )
        return json.loads(response["message"]["content"])
    except ConnectionError:
        # 1. Ollama is not running
        raise SystemExit("[Error] Cannot reach Ollama — start it first.")
    except ollama.ResponseError as e:
        # 2. Model not pulled / bad request — e.g. "model 'xx' not found (status code: 404)"
        raise SystemExit(f"[Error] {e.error}")
    except json.JSONDecodeError:
        # 3. Output was not the JSON we hoped for
        return {"sentiment": "unknown", "category": "unknown"}
```

And the failure no `except` can catch: **the model answered fluently and was wrong.** Treat LLM output the way you treat user input — validate what you can, never execute it blindly, and keep a human in the loop for decisions that matter.

---

### Streaming — Watching the Answer Arrive

By default `ollama.chat` waits for the *complete* answer — on a slow laptop a long reply means ten silent seconds. `stream=True` returns chunks as they are generated, like ChatGPT's typing effect:

```python
for chunk in ollama.chat(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "Suggest three ways to practice Python."}],
    stream=True,
):
    print(chunk["message"]["content"], end="", flush=True)   # No newline between chunks
print()
```

Rule of thumb: **streaming for humans watching, non-streaming for scripts parsing.** (You cannot `json.loads` half an answer — batch jobs like the Guided Practice use `stream=False`.)

---

## Going Further

<details>
<summary>The Raw REST API — No Package Required</summary>

Everything the `ollama` package does, `requests` can do directly — useful on machines where you cannot install extra packages, or just to prove there is no magic:

```python
import requests

resp = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen2.5:7b",
        "messages": [{"role": "user", "content": "What is an API?"}],
        "stream": False,
    },
    timeout=120,    # Local models can be slow on modest hardware
)
resp.raise_for_status()
print(resp.json()["message"]["content"])
```

</details>

<details>
<summary>Tuning Generation with options</summary>

```python
options={
    "temperature": 0.2,   # 0 = deterministic, ~1 = creative
    "num_predict": 200,   # Cap the reply length (tokens)
    "num_ctx": 8192,      # Context window — how much input the model can see
}
```

If long prompts seem "forgotten", you ran past `num_ctx` — the model literally never saw the start of your text.

</details>

<details>
<summary>Vision — Models That Read Images</summary>

Multimodal models accept image files alongside text:

```python
response = ollama.chat(
    model="gemma3:4b",     # A vision-capable model (ollama pull gemma3:4b)
    messages=[{
        "role": "user",
        "content": "Describe this image in one paragraph.",
        "images": ["photo.jpg"],
    }],
)
```

Receipt readers, photo organizers, chart describers — same pattern, one extra key.

</details>

<details>
<summary>Same Pattern, Cloud Models</summary>

The `messages`/roles structure you learned here is the de-facto industry standard — OpenAI, Anthropic, and Google APIs all look nearly identical. Swap the client and add an API key, and your Ollama code becomes cloud code. Learn once, call anything.

</details>

<details>
<summary>Choosing Models — ollama.com/library</summary>

Browse **[ollama.com/library](https://ollama.com/library)**. Reading a listing: `7b` = 7 billion parameters (bigger = smarter = slower = more RAM); tags like `instruct` (tuned to follow instructions — what you want) vs `base` (raw text predictor — not what you want). Rough RAM rule: model file size + 2–3 GB headroom.

</details>

<details>
<summary>Combining Modules in a Pipeline</summary>

The real power comes from chaining modules:
- **M11 (requests):** fetch data to process
- **M16 (Ollama):** classify or summarize each item
- **M12 (SQLite):** store the results
- **M15 (pandas):** analyze and chart what accumulated

This is the architecture of a real data-enrichment pipeline.

</details>

---

## Guided Practice

**Scenario:** a cafe owner hands you `reviews.csv` (in this folder) — 40 free-text customer reviews. She wants to know: *is feedback mostly positive? What do unhappy customers complain about?* No loop or `if` can read prose — and doing it by hand means reading all 40, judging each one, and typing the verdicts into a spreadsheet: half an hour of mind-numbing clerical work, with drifting standards as you get bored. You will build an **AI review analyzer** instead: each review goes to the local LLM, comes back as structured JSON, and a counting loop turns the pile into answers — a few unattended minutes, identical criteria for review #1 and review #40. And when next month brings 400 reviews, the same script still costs you zero extra effort.

The finished script is `review_analyzer_example.py`. Build it step by step:

### Step 1 — Smoke test the connection

Create `review_analyzer_example.py`. Before building anything, prove the plumbing works:

```python
import ollama

response = ollama.chat(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "Say one short sentence to prove you are alive."}],
)
print(response["message"]["content"])
```

Run it. If you get a sentence, the whole stack works — Python → Ollama server → model → back. If it dies with `ConnectionError`, start Ollama; with `ResponseError ... not found`, you have not pulled the model.

### Step 2 — Design the prompt

The prompt is the heart of the tool — role + task + exact output shape, with the review text injected by `str.format()` (the doubled `{{ }}` braces survive as literal braces):

```python
PROMPT_TEMPLATE = """You are a review analyst for the restaurant industry.
Analyze the customer review below. Reply with ONLY JSON, no other text,
in exactly this format:
{{"sentiment": "positive, negative or neutral",
  "category": "food, service, environment or price",
  "summary": "a summary in ten words or fewer"}}

"category" MUST be exactly one of: food, service, environment, price.
Pick the closest one.

Review: "{review}\""""
```

Map this onto the four building blocks from Core Concepts: the **context** ("You are a review analyst...", plus the review itself at the bottom), the **instruction** ("Analyze the customer review below"), and the **constraints** ("ONLY JSON", the exact key shape, the MUST list). One block is missing — **examples**. That is a deliberate choice, not an oversight: `format="json"` plus tight constraints already pin the output down, and each example would be re-sent on every one of the 40 calls. Start without examples; add one only if the model strays.

That blunt `MUST be exactly one of` line earned its place: without it, this exact script once classified a review's category as `"overall experience"` — a value we never offered. `format="json"` guaranteed the *syntax*; only the prompt pins down the *values*. When a model strays, tighten the prompt.

### Step 3 — Wrap the call in a defensive function

```python
import json

def analyze_review(review: str) -> dict:
    """Send one review to the local LLM and return the parsed verdict."""
    try:
        resp = ollama.chat(
            model="qwen2.5:7b",
            messages=[{"role": "user",
                       "content": PROMPT_TEMPLATE.format(review=review)}],
            format="json",                  # Valid JSON syntax, guaranteed
            options={"temperature": 0},     # Same review → same verdict
        )
        return json.loads(resp["message"]["content"])
    except ConnectionError:
        raise SystemExit("[Error] Cannot reach Ollama — start Ollama first.")
    except ollama.ResponseError as e:
        raise SystemExit(f"[Error] {e.error} — did you `ollama pull qwen2.5:7b`?")
    except json.JSONDecodeError:
        return {"sentiment": "unknown", "category": "unknown",
                "summary": "(could not parse model output)"}
```

Test it on one review before looping — always:

```python
print(analyze_review("Waited twenty-five minutes for my food "
                     "and the staff never even apologized."))
# → {'sentiment': 'negative', 'category': 'service', 'summary': 'Long wait no apology'}
```

### Step 4 — Loop over the CSV

M10's `csv.DictReader` loads the reviews, a plain `for` loop feeds them to the model (M05). As each verdict comes back, `row.update(verdict)` bolts the three new keys onto the original row — text and judgment travel together from here on. Print progress as you go — at a few seconds per review, a silent loop feels broken:

```python
import csv

with open("reviews.csv", encoding="utf-8-sig", newline="") as f:
    reviews = list(csv.DictReader(f))

print(f"Analyzing {len(reviews)} reviews — local models take a moment per review...\n")

report = []
for i, row in enumerate(reviews, start=1):
    verdict = analyze_review(row["review"])
    row.update(verdict)         # Verdict columns join the original columns
    report.append(row)
    print(f"[{i:>2}/{len(reviews)}] {row['sentiment']:<8} | "
          f"{row['category']:<11} | {row['summary']}")
```

```
[ 1/40] positive | food        | Excellent coffee quality
[ 2/40] negative | service     | Long wait no apology
[ 3/40] neutral  | environment | Good for working quietly
[ 4/40] negative | price       | Expensive drink
...
[26/40] negative | food        | Hair found in sandwich
...
[40/40] positive | price       | Fair prices with reliable quality
```

Go get some water and watch it work through the pile. Forty pieces of prose are becoming forty rows of data — the boring half hour the owner dreaded, running by itself while you stretch.

### Step 5 — Summarize and export

`report` is a list of dictionaries, and the owner's questions are counting questions — M04's `dict.get()` trick handles them. Write one small helper instead of two copy-pasted loops (M06's DRY principle):

```python
def count_by(rows: list, key: str) -> dict:
    """Count how many rows share each value of `key`, e.g. {'negative': 18}."""
    counts = {}
    for row in rows:
        value = row[key]
        counts[value] = counts.get(value, 0) + 1
    return counts
```

Export the enriched table with M10's `csv.DictWriter`, then answer the questions:

```python
with open("reviews_analyzed.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=report[0].keys())
    writer.writeheader()
    writer.writerows(report)

print("\n=== Sentiment overview ===")
sentiments = count_by(report, "sentiment")
for sentiment in sorted(sentiments, key=sentiments.get, reverse=True):
    print(f"{sentiment:<10} {sentiments[sentiment]}")

print("\n=== What do negative reviews complain about? ===")
negative_rows = []
for row in report:
    if row["sentiment"] == "negative":
        negative_rows.append(row)
categories = count_by(negative_rows, "category")
for category in sorted(categories, key=categories.get, reverse=True):
    print(f"{category:<12} {categories[category]}")
```

(`sorted(sentiments, key=sentiments.get, reverse=True)` sorts the dictionary's keys by their counts, biggest first — handy for any "ranking" printout.)

```
=== Sentiment overview ===
negative   18
positive   15
neutral    7

=== What do negative reviews complain about? ===
food         6
service      4
price        4
environment  4
```

The owner's answer, measured: feedback leans negative, and food complaints lead. Open `reviews_analyzed.csv` in Excel and admire it: original text on the left, machine-readable verdicts on the right — the spreadsheet she would have spent her evening typing. You have built a pipeline no module could build alone — M10's CSV and JSON, M11's API thinking, M08's defensive calls, and an AI that reads. **That is Zero to One.** (And if you want charts of these counts, the `report` list is one `pd.DataFrame(report)` away from everything you learned in M15.)

### Step 6 — Break it on purpose

Three experiments, one minute each:

1. Quit Ollama and run the script — confirm your `ConnectionError` message appears instead of a traceback.
2. Change the model name to `qwen99` — confirm the `ResponseError` path.
3. Set `temperature` to `1.0` and rerun twice — watch verdicts wobble between runs, then put `0` back. Now you know *why* it was there.

---

## Checkpoints

* [ ] **Polite Email Polisher**
  Build a tool that rewrites blunt emails. System prompt: an experienced customer-success specialist; rule: return ONLY the rewritten email, keeping the original meaning.
  Test with contrasting drafts like `"Refund not possible. Ticket closed."` and `"I can't finish the report today. I'll do it whenever I have time."`.
  Then delete the system prompt and rerun — observe concretely what it was doing for you.

* [ ] **Local Code Reviewer**
  Read any of your earlier `.py` files (path from `input()`), send the code to the LLM, and ask for the top 3 concrete improvements referencing specific function names or line numbers.
  Use `stream=True` so the review types out live.
  Judge the output critically: which suggestions are genuinely useful, and which are confident nonsense?

* [ ] **Daily News Digest with Sentiment**
  Combine M11 + M12 + M16.
  Fetch the top 5 headlines from `https://hn.algolia.com/api/v1/search?tags=front_page` (Hacker News, no key needed).
  For each, have the LLM return JSON: a sentiment (`positive`/`negative`/`neutral`) and a one-sentence summary.
  Store everything in a SQLite table `headlines(id, fetched_on, title, sentiment, summary)`.
  Print: `"Today's mood: 3 positive, 1 neutral, 1 negative."`
  Bonus: after collecting a few days, chart the sentiment mix over time with M15's pandas.
