const config = {
  port: Number(process.env.PORT || 3000),
  bioMistralApiUrl: process.env.BIOMISTRAL_API_URL || "",
  bioMistralApiKey: process.env.BIOMISTRAL_API_KEY || "",
  afriSpeechTtsUrl: process.env.AFRISPEECH_TTS_URL || "",
  afriSpeechApiKey: process.env.AFRISPEECH_API_KEY || ""
};

module.exports = config;
