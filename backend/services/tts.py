from functools import lru_cache
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import wave
import tempfile
import os

from piper import PiperVoice, SynthesisConfig

from backend.config import Config


@lru_cache(maxsize=1)
def _load_tts_voice() -> PiperVoice:
    model_path = Config.afro_tts_model_path.strip()
    if not model_path:
        raise ValueError("AFRO_TTS_MODEL_PATH is not configured.")

    config_path = Config.afro_tts_config_path.strip() or None
    return PiperVoice.load(model_path=model_path, config_path=config_path, use_cuda=Config.afro_tts_use_cuda)


def synthesize_with_afri_speech(text: str) -> Tuple[Dict[str, object], bytes]:
    content = str(text or "").strip()
    if not content:
        return {"ok": False, "status": 400, "message": "Text is required for speech synthesis."}, b""

    try:
        voice = _load_tts_voice()
        wav_buffer = BytesIO()
        with wave.open(wav_buffer, "wb") as wav_file:
            voice.synthesize_wav(
                content,
                wav_file,
                syn_config=SynthesisConfig(),
                set_wav_format=True,
            )

        return {"ok": True, "status": 200, "mime_type": "audio/wav"}, wav_buffer.getvalue()
    except (OSError, ValueError, TypeError, RuntimeError, AttributeError, KeyError):
        return {"ok": False, "status": 500, "message": "Could not synthesize speech with the local Piper model."}, b""


@lru_cache(maxsize=1)
def _load_xtts():
    model_id = Config.xtts_model_id.strip()
    if not model_id:
        raise ValueError("XTTS_MODEL_ID is not configured.")

    # Prefer the newer Coqui X-TTS v2 package if available, else fall back to the
    # legacy `TTS` package. This keeps the integration resilient across
    # different environments while preferring `xtts` when installed.
    try:
        # try importing the xtts package (Coqui X-TTS v2)
        import xtts as _xtts_pkg

        # common loader helpers: try several sensible entrypoints
        if hasattr(_xtts_pkg, "load_model"):
            return _xtts_pkg.load_model(model_id, device=("cuda" if Config.xtts_use_cuda else "cpu"))

        if hasattr(_xtts_pkg, "XTTS"):
            # XTTS class-style API (best-effort)
            return _xtts_pkg.XTTS(model_name=model_id, device=("cuda" if Config.xtts_use_cuda else "cpu"))

        # If package exists but no known entrypoint, raise to fall back below
        raise ImportError("Installed xtts package does not expose a known loader API.")
    except Exception:
        # fallback to the classical Coqui TTS package (package name: TTS)
        try:
            from TTS.api import TTS
        except Exception as exc:  # ImportError or others
            raise ImportError("Coqui X-TTS is not installed. Install 'xtts' or 'TTS'.") from exc

        # instantiate TTS model (gpu flag depends on Config)
        return TTS(model_name=model_id, progress_bar=False, gpu=Config.xtts_use_cuda)


def synthesize_with_xtts(text: str, speaker_wav: Optional[str] = None, language: Optional[str] = None) -> Tuple[Dict[str, object], bytes]:
    content = str(text or "").strip()
    if not content:
        return {"ok": False, "status": 400, "message": "Text is required for speech synthesis."}, b""

    try:
        tts = _load_xtts()

        # write to a temporary wav file using the TTS helper, then return bytes
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp_path = tmp.name

        try:
            # TTS.tts_to_file will create the file at tmp_path. Pass optional
            # speaker_wav and language args when provided to support voice
            # cloning / multilingual synthesis in X-TTS v2.
            tts_kwargs = {}
            if speaker_wav:
                tts_kwargs["speaker_wav"] = speaker_wav
            if language:
                tts_kwargs["language"] = language

            # TTS.tts_to_file will create the file at tmp_path
            tts.tts_to_file(text=content, file_path=tmp_path, **tts_kwargs)
            with open(tmp_path, "rb") as f:
                data = f.read()
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        return {"ok": True, "status": 200, "mime_type": "audio/wav"}, data
    except (ImportError, OSError, ValueError, TypeError, RuntimeError, AttributeError, KeyError) as e:
        return {"ok": False, "status": 500, "message": f"Could not synthesize speech with Coqui X-TTS: {e}"}, b""


def synthesize(text: str, speaker_wav: Optional[str] = None, language: Optional[str] = None) -> Tuple[Dict[str, object], bytes]:
    """Unified entrypoint: use Coqui X-TTS when enabled, otherwise fall back to Piper.

    `speaker_wav` and `language` are optional and passed only to X-TTS; the
    local Piper backend does not support voice cloning and will ignore them.
    """
    if getattr(Config, "xtts_enabled", False):
        return synthesize_with_xtts(text, speaker_wav=speaker_wav, language=language)
    return synthesize_with_afri_speech(text)
