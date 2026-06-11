"""Guided Practice — An AI-powered customer review analyzer.

Scenario: a cafe owner has a pile of free-text customer reviews
(`reviews.csv`) and wants to know, without reading every one:
  * Is the feedback mostly positive or negative?
  * What are people complaining about — the food, the service,
    the environment, or the price?

No traditional program can read prose. A local LLM can. This script:
  1. Sends each review to a local model via Ollama
  2. Forces the answer into JSON (sentiment / category / summary)
  3. Collects every verdict next to its original review (M10's csv)
  4. Prints a summary and exports an enriched CSV

Before running:
  * Install Ollama from https://ollama.com and pull the model:
      ollama pull qwen2.5:7b
  * pip install ollama

Run from this folder:  python review_analyzer_example.py
Output: reviews_analyzed.csv
"""

import csv
import json

import ollama

MODEL = "qwen2.5:7b"

# The {{ }} doubles are literal braces in the prompt; {review} is filled in.
PROMPT_TEMPLATE = """You are a review analyst for the restaurant industry.
Analyze the customer review below. Reply with ONLY JSON, no other text,
in exactly this format:
{{"sentiment": "positive, negative or neutral",
  "category": "food, service, environment or price",
  "summary": "a summary in ten words or fewer"}}

"category" MUST be exactly one of: food, service, environment, price.
Pick the closest one.

Review: "{review}\""""


def analyze_review(review: str) -> dict:
    """Send one review to the local LLM and return the parsed verdict."""
    try:
        resp = ollama.chat(
            model=MODEL,
            messages=[{"role": "user",
                       "content": PROMPT_TEMPLATE.format(review=review)}],
            format="json",                  # Ollama guarantees valid JSON syntax
            options={"temperature": 0},     # Classification wants consistency
        )
        return json.loads(resp["message"]["content"])
    except ConnectionError:
        raise SystemExit("[Error] Cannot reach Ollama — start Ollama first.")
    except ollama.ResponseError as e:
        raise SystemExit(f"[Error] {e.error} — did you `ollama pull {MODEL}`?")
    except json.JSONDecodeError:
        # format="json" makes this rare, but defensive code assumes nothing.
        return {"sentiment": "unknown", "category": "unknown",
                "summary": "(could not parse model output)"}


def count_by(rows: list, key: str) -> dict:
    """Count how many rows share each value of `key`, e.g. {'negative': 18}."""
    counts = {}
    for row in rows:
        value = row[key]
        counts[value] = counts.get(value, 0) + 1
    return counts


with open("reviews.csv", encoding="utf-8-sig", newline="") as f:
    reviews = list(csv.DictReader(f))

print(f"Analyzing {len(reviews)} reviews with {MODEL} — "
      f"local models take a moment per review...\n")

report = []
for i, row in enumerate(reviews, start=1):
    verdict = analyze_review(row["review"])
    row.update(verdict)         # Verdict columns join the original columns
    report.append(row)
    print(f"[{i:>2}/{len(reviews)}] {row['sentiment']:<8} | "
          f"{row['category']:<11} | {row['summary']}")

# Write the enriched table back out — original text plus the three verdicts
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

print("\nSaved: reviews_analyzed.csv")
