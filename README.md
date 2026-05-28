# medictest

AI-integrated medical voice assistant with:
- **BioMistral** reasoning (backend integration)
- **AfriSpeech** text-to-speech (backend integration)
- Voice input + voice output frontend

## Project structure

```text
backend/
  src/
    app.js
    server.js
    config.js
    services/
      reasoning.js
      tts.js
frontend/
  index.html
  app.js
  styles.css
test/
  app.test.js
```

## Setup

```bash
npm install
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
npm start
```

Open `http://localhost:3000`.

## Test

```bash
npm test
```
