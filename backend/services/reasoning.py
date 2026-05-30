from functools import lru_cache
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from backend.config import Config

torch_api: Any = torch

FALLBACK_RESPONSE = (
    "I can help with general medical information, but I am not a substitute for a licensed clinician. "
    "Please share your symptoms and duration, and seek urgent care immediately for severe pain, chest pain, breathing difficulty, or loss of consciousness."
)
SYSTEM_PROMPT = (
    """You are a professional medical assistant. Provide concise, non-diagnostic guidance and encourage urgent care for severe symptoms.
        critical rules:
        * Don't give advice that is dangerous and self medicative
        * Don't give any sucaidal advice
        * If not related to medicine, tell them politely that you were built to just assist medically
    
    """
)


@lru_cache(maxsize=1)
def _load_model() -> tuple[Any, Any]:
    tokenizer = AutoTokenizer.from_pretrained(
        Config.bio_mistral_model_id,
        local_files_only=Config.bio_mistral_local_files_only,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token or tokenizer.unk_token

    model = AutoModelForCausalLM.from_pretrained(
        Config.bio_mistral_model_id,
        local_files_only=Config.bio_mistral_local_files_only,
        torch_dtype=torch_api.float16 if torch_api.cuda.is_available() else torch_api.float32,
    )
    model.to("cuda" if torch_api.cuda.is_available() else "cpu")
    model.eval()
    return tokenizer, model


def _build_inputs(tokenizer: Any, prompt: str, model: Any) -> dict[str, Any]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    if hasattr(tokenizer, "apply_chat_template"):
        encoded = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )
    else:
        encoded = tokenizer(
            f"{SYSTEM_PROMPT}\n\nUser: {prompt}\nAssistant:",
            return_tensors="pt",
        )

    return {key: value.to(model.device) for key, value in encoded.items()}


def get_bio_mistral_response(prompt: str) -> str:
    cleaned_prompt = str(prompt or "").strip()
    if not cleaned_prompt:
        return "Please say or type your medical question so I can assist."

    try:
        tokenizer, model = _load_model()
        inputs = _build_inputs(tokenizer, cleaned_prompt, model)
        with torch_api.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=Config.bio_mistral_max_new_tokens,
                do_sample=True,
                temperature=Config.bio_mistral_temperature,
                top_p=Config.bio_mistral_top_p,
                pad_token_id=tokenizer.pad_token_id,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        reply = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        return reply or FALLBACK_RESPONSE
    except (OSError, ValueError, TypeError, RuntimeError, AttributeError):
        return FALLBACK_RESPONSE
