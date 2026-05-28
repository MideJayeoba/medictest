const path = require("path");
const express = require("express");
const { getBioMistralResponse } = require("./services/reasoning");
const { synthesizeWithAfriSpeech } = require("./services/tts");

const app = express();

app.use(express.json({ limit: "10kb" }));
app.use(express.static(path.resolve(__dirname, "../../frontend")));

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.post("/api/assistant/respond", async (req, res) => {
  const input = String(req.body?.input || "").trim();
  if (!input) {
    return res.status(400).json({ error: "Voice or text input is required." });
  }

  if (input.length > 2000) {
    return res.status(400).json({ error: "Input is too long." });
  }

  const reply = await getBioMistralResponse(input);
  return res.json({ reply, model: "BioMistral" });
});

app.post("/api/tts", async (req, res) => {
  const result = await synthesizeWithAfriSpeech(req.body?.text);
  if (!result.ok) {
    return res.status(result.status).json({ error: result.message });
  }

  res.setHeader("Content-Type", result.mimeType);
  return res.send(result.buffer);
});

module.exports = app;
