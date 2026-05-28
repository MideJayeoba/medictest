import os


class Config:
    port = int(os.getenv("PORT", "3000"))
    bio_mistral_api_url = os.getenv("BIOMISTRAL_API_URL", "")
    bio_mistral_api_key = os.getenv("BIOMISTRAL_API_KEY", "")
    afri_speech_tts_url = os.getenv("AFRISPEECH_TTS_URL", "")
    afri_speech_api_key = os.getenv("AFRISPEECH_API_KEY", "")
