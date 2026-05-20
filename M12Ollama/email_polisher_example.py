"""Guided Practice 1 — Rewrite a blunt email into a professional one.

Scenario: a colleague writes technically correct but cold emails to
customers. We feed the rough draft into a local LLM and ask it to
return a warmer, clearer version while keeping the original meaning.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def polish_email(raw_text: str) -> str:
    """Send the draft to Ollama and return the polished version (or an error)."""
    prompt = (
        "You are an experienced customer-success specialist.\n"
        "Rewrite the following email so it is polite, warm, and clear.\n"
        "Keep the original meaning. Do NOT add any commentary or headers — "
        "return ONLY the rewritten email body.\n\n"
        "Original email:\n"
        f"{raw_text}\n"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=120,   # local models can take a while on small machines
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        return "[Error] Cannot reach Ollama. Is it running?"
    except requests.exceptions.HTTPError as err:
        return f"[Error] Ollama returned {err.response.status_code}. Did you `ollama pull {MODEL}`?"
    except requests.exceptions.Timeout:
        return "[Error] The model took too long. Try a smaller model or a shorter prompt."


# Two drafts that show different "problems" — too curt, and too technical.
drafts = [
    "Refund not possible. Read the FAQ. Closing this ticket.",
    "Your auth token expired so the API rejected the request — regenerate it in /settings.",
]

for i, draft in enumerate(drafts, start=1):
    print(f"\n--- Draft #{i} ---\n{draft}")
    print(f"\n--- Polished #{i} ---\n{polish_email(draft)}")
