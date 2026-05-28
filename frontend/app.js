const inputText = document.getElementById("inputText");
const responseText = document.getElementById("responseText");
const listenBtn = document.getElementById("listenBtn");
const sendBtn = document.getElementById("sendBtn");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    inputText.value = event.results[0][0].transcript;
  };

  recognition.onerror = () => {
    responseText.textContent = "Voice recognition failed. You can type your question and send it.";
  };
} else {
  listenBtn.disabled = true;
  listenBtn.textContent = "🎙️ Voice not supported";
}

listenBtn.addEventListener("click", () => {
  if (recognition) {
    recognition.start();
  }
});

sendBtn.addEventListener("click", async () => {
  const input = inputText.value.trim();
  if (!input) {
    responseText.textContent = "Please speak or type a message first.";
    return;
  }

  responseText.textContent = "Thinking...";

  try {
    const response = await fetch("/api/assistant/respond", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input })
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Assistant request failed.");
    }

    responseText.textContent = data.reply;
    await playSpeech(data.reply);
  } catch (error) {
    responseText.textContent = error.message;
  }
});

async function playSpeech(text) {
  try {
    const response = await fetch("/api/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      throw new Error();
    }

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
    audio.onended = () => URL.revokeObjectURL(audioUrl);
  } catch {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(new SpeechSynthesisUtterance(text));
    }
  }
}
