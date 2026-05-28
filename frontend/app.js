const { useEffect, useRef, useState } = React;

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("Waiting for input...");
  const [voiceSupported, setVoiceSupported] = useState(true);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setVoiceSupported(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = (event) => {
      setInput(event.results[0][0].transcript);
    };
    recognition.onerror = () => {
      setResponse("Voice recognition failed. You can type your question and send it.");
    };
    recognitionRef.current = recognition;
  }, []);

  const listen = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    }
  };

  const playSpeech = async (text) => {
    try {
      const ttsResponse = await fetch("/api/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (!ttsResponse.ok) {
        throw new Error("TTS unavailable");
      }

      const audioBlob = await ttsResponse.blob();
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
  };

  const sendInput = async () => {
    const value = input.trim();
    if (!value) {
      setResponse("Please speak or type a message first.");
      return;
    }

    setResponse("Thinking...");
    try {
      const apiResponse = await fetch("/api/assistant/respond", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input: value }),
      });
      const data = await apiResponse.json();
      if (!apiResponse.ok) {
        throw new Error(data.error || "Assistant request failed.");
      }

      setResponse(data.reply);
      await playSpeech(data.reply);
    } catch (error) {
      setResponse(error.message);
    }
  };

  return (
    <main className="container">
      <h1>medictest Voice Assistant</h1>
      <p>
        Speak your medical question. The assistant reasons with BioMistral and returns voice output via
        AfriSpeech (or browser fallback).
      </p>

      <section className="panel">
        <label htmlFor="inputText">Captured input</label>
        <textarea
          id="inputText"
          rows="4"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Your voice input appears here..."
        />
        <div className="actions">
          <button type="button" disabled={!voiceSupported} onClick={listen}>
            {voiceSupported ? "🎙️ Start listening" : "🎙️ Voice not supported"}
          </button>
          <button type="button" onClick={sendInput}>
            Send
          </button>
        </div>
      </section>

      <section className="panel">
        <h2>Assistant response</h2>
        <p>{response}</p>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
