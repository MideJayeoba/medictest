const config = require("../config");

const FALLBACK_RESPONSE =
  "I can help with general medical information, but I am not a substitute for a licensed clinician. " +
  "Please share your symptoms and duration, and seek urgent care immediately for severe pain, chest pain, breathing difficulty, or loss of consciousness.";

async function getBioMistralResponse(prompt) {
  const cleanedPrompt = String(prompt || "").trim();
  if (!cleanedPrompt) {
    return "Please say or type your medical question so I can assist.";
  }

  if (!config.bioMistralApiUrl || !config.bioMistralApiKey) {
    return FALLBACK_RESPONSE;
  }

  try {
    const response = await fetch(config.bioMistralApiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + config.bioMistralApiKey
      },
      body: JSON.stringify({
        inputs: `You are a cautious medical assistant. Provide concise, non-diagnostic guidance. User: ${cleanedPrompt}`,
        options: { wait_for_model: true }
      })
    });

    if (!response.ok) {
      return FALLBACK_RESPONSE;
    }

    const body = await response.json();
    const generated = Array.isArray(body)
      ? body[0]?.generated_text
      : body?.generated_text || body?.text;

    return String(generated || FALLBACK_RESPONSE).trim();
  } catch {
    return FALLBACK_RESPONSE;
  }
}

module.exports = { getBioMistralResponse, FALLBACK_RESPONSE };
