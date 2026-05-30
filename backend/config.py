import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    port = int(os.getenv("PORT", "3000"))
    bio_mistral_model_id = os.getenv("BIOMISTRAL_MODEL_ID", "BioMistral/BioMistral-7B")
    bio_mistral_local_files_only = os.getenv("BIOMISTRAL_LOCAL_FILES_ONLY", "false").lower() == "true"
    bio_mistral_max_new_tokens = int(os.getenv("BIOMISTRAL_MAX_NEW_TOKENS", "128"))
    bio_mistral_temperature = float(os.getenv("BIOMISTRAL_TEMPERATURE", "0.3"))
    bio_mistral_top_p = float(os.getenv("BIOMISTRAL_TOP_P", "0.9"))
    afro_tts_model_path = os.getenv("AFRO_TTS_MODEL_PATH", "")
    afro_tts_config_path = os.getenv("AFRO_TTS_CONFIG_PATH", "")
    afro_tts_use_cuda = os.getenv("AFRO_TTS_USE_CUDA", "false").lower() == "true"
    # Coqui X-TTS v2 (optional)
    xtts_enabled = os.getenv("XTTS_ENABLED", "false").lower() == "true"
    xtts_model_id = os.getenv("XTTS_MODEL_ID", "")
    xtts_use_cuda = os.getenv("XTTS_USE_CUDA", "false").lower() == "true"
