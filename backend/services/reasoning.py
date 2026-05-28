import requests

from backend.config import Config

FALLBACK_RESPONSE = (
    "I can help with general medical information, but I am not a substitute for a licensed clinician. "
    "Please share your symptoms and duration, and seek urgent care immediately for severe pain, chest pain, breathing difficulty, or loss of consciousness."
)


def get_bio_mistral_response(prompt: str) -> str:
    cleaned_prompt = str(prompt or "").strip()
    if not cleaned_prompt:
        return "Please say or type your medical question so I can assist."

    if not Config.bio_mistral_api_url or not Config.bio_mistral_api_key:
        return FALLBACK_RESPONSE

    try:
        response = requests.post(
            Config.bio_mistral_api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + Config.bio_mistral_api_key,
            },
            json={
                "inputs": "You are a cautious medical assistant. Provide concise, non-diagnostic guidance. "
                f"User: {cleaned_prompt}",
                "options": {"wait_for_model": True},
            },
            timeout=20,
        )
        if not response.ok:
            return FALLBACK_RESPONSE

        body = response.json()
        generated = None
        if isinstance(body, list) and body:
            generated = body[0].get("generated_text")
        elif isinstance(body, dict):
            generated = body.get("generated_text") or body.get("text")

        return str(generated or FALLBACK_RESPONSE).strip()
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return FALLBACK_RESPONSE
