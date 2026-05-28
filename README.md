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

Optional environment variables:

- `PORT` (default: `3000`)
- `BIOMISTRAL_API_URL`
- `BIOMISTRAL_API_KEY`
- `AFRISPEECH_TTS_URL`
- `AFRISPEECH_API_KEY`

If BioMistral/AfriSpeech are not configured, the app uses safe fallbacks.

## Run

```bash
python -m backend.server
```

Open `http://localhost:3000`.

## Test

```bash
python -m unittest discover -s tests
```
