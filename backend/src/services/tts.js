const config = require("../config");

async function synthesizeWithAfriSpeech(text) {
  const content = String(text || "").trim();
  if (!content) {
    return { ok: false, status: 400, message: "Text is required for speech synthesis." };
  }

  if (!config.afriSpeechTtsUrl || !config.afriSpeechApiKey) {
    return {
      ok: false,
      status: 501,
      message: "AfriSpeech TTS is not configured. Set AFRISPEECH_TTS_URL and AFRISPEECH_API_KEY."
    };
  }

  try {
    const response = await fetch(config.afriSpeechTtsUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + config.afriSpeechApiKey
      },
      body: JSON.stringify({ text: content })
    });

    if (!response.ok) {
      return { ok: false, status: response.status, message: "AfriSpeech TTS request failed." };
    }

    const arrayBuffer = await response.arrayBuffer();
    return {
      ok: true,
      status: 200,
      mimeType: response.headers.get("content-type") || "audio/mpeg",
      buffer: Buffer.from(arrayBuffer)
    };
  } catch {
    return { ok: false, status: 502, message: "Could not reach AfriSpeech TTS service." };
  }
}

module.exports = { synthesizeWithAfriSpeech };
