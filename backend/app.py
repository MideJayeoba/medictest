from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from backend.services.reasoning import get_bio_mistral_response
from backend.services.tts import synthesize_with_afri_speech

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(__name__, static_folder=str(frontend_dir), static_url_path="")


@app.get("/")
def serve_frontend():
    return send_from_directory(frontend_dir, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/assistant/respond")
def assistant_respond():
    body = request.get_json(silent=True) or {}
    input_text = str(body.get("input", "")).strip()

    if not input_text:
        return jsonify({"error": "Voice or text input is required."}), 400
    if len(input_text) > 2000:
        return jsonify({"error": "Input is too long."}), 400

    reply = get_bio_mistral_response(input_text)
    return jsonify({"reply": reply, "model": "BioMistral"})


@app.post("/api/tts")
def tts():
    body = request.get_json(silent=True) or {}
    result, audio_bytes = synthesize_with_afri_speech(body.get("text"))
    if not result.get("ok"):
        return jsonify({"error": result["message"]}), int(result["status"])

    return audio_bytes, 200, {"Content-Type": str(result["mime_type"])}


@app.get("/<path:filename>")
def static_files(filename: str):
    return send_from_directory(frontend_dir, filename)
