# medictest

AI-integrated medical voice assistant with:

- **BioMistral** reasoning (backend integration)
- **AfriSpeech** text-to-speech (backend integration)
- Voice input + voice output frontend

## Project structure

```text
backend/
  app.py
  config.py
  server.py
  services/
    reasoning.py
    tts.py
frontend/
  index.html
  app.js
  styles.css
tests/
  test_app.py
requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root using the template below, then fill in your local model paths.

```bash
PORT=3000
BIOMISTRAL_MODEL_ID=BioMistral/BioMistral-7B
BIOMISTRAL_LOCAL_FILES_ONLY=false
BIOMISTRAL_MAX_NEW_TOKENS=128
BIOMISTRAL_TEMPERATURE=0.3
BIOMISTRAL_TOP_P=0.9
AFRO_TTS_MODEL_PATH=/absolute/path/to/your/piper/model.onnx
AFRO_TTS_CONFIG_PATH=
AFRO_TTS_USE_CUDA=false
```

Environment variables:

- `PORT` (default: `3000`)
- `BIOMISTRAL_MODEL_ID` for a Hugging Face model ID or a local fine-tuned checkpoint path
- `BIOMISTRAL_LOCAL_FILES_ONLY` set to `true` if the model is already on disk
- `BIOMISTRAL_TEMPERATURE`
- `BIOMISTRAL_MAX_NEW_TOKENS`
- `BIOMISTRAL_TOP_P`
- `AFRO_TTS_MODEL_PATH` for the local Piper `.onnx` checkpoint
- `AFRO_TTS_CONFIG_PATH` if the model config is stored separately
- `AFRO_TTS_USE_CUDA` set to `true` if you have a CUDA-capable build

If the reasoning model cannot be loaded, the backend returns a safe medical fallback message instead of failing.
If the local Piper model cannot be loaded, `/api/tts` returns a synthesis error instead of crashing.

## Run

```bash
python -m backend.server
```

Open `http://localhost:3000`.

## Test

```bash
python -m unittest discover -s tests
```

The backend now runs on FastAPI, with the same `/api/*` routes and the frontend still served from `/`.
