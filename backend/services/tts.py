from typing import Dict, Tuple

import requests

from backend.config import Config


def synthesize_with_afri_speech(text: str) -> Tuple[Dict[str, object], bytes]:
    content = str(text or "").strip()
    if not content:
        return {"ok": False, "status": 400, "message": "Text is required for speech synthesis."}, b""

    if not Config.afri_speech_tts_url or not Config.afri_speech_api_key:
        return {
            "ok": False,
            "status": 501,
            "message": "AfriSpeech TTS is not configured. Set AFRISPEECH_TTS_URL and AFRISPEECH_API_KEY.",
        }, b""

    try:
        response = requests.post(
            Config.afri_speech_tts_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + Config.afri_speech_api_key,
            },
            json={"text": content},
            timeout=20,
        )
        if not response.ok:
            return {"ok": False, "status": response.status_code, "message": "AfriSpeech TTS request failed."}, b""

        return {
            "ok": True,
            "status": 200,
            "mime_type": response.headers.get("content-type", "audio/mpeg"),
        }, response.content
    except requests.RequestException:
        return {"ok": False, "status": 502, "message": "Could not reach AfriSpeech TTS service."}, b""
