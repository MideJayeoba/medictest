from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from backend.services.reasoning import get_bio_mistral_response
from backend.services.tts import synthesize

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app = FastAPI()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/assistant/respond")
def assistant_respond(payload: dict[str, Any] | None = Body(default=None)):
    body = payload or {}
    input_text = str(body.get("input", "")).strip()

    if not input_text:
        return JSONResponse({"error": "Voice or text input is required."}, status_code=400)
    if len(input_text) > 2000:
        return JSONResponse({"error": "Input is too long."}, status_code=400)

    reply = get_bio_mistral_response(input_text)
    return {"reply": reply, "model": "BioMistral"}


@app.post("/api/tts")
async def tts(
    payload: dict[str, Any] | None = Body(default=None),
    speaker_file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
    language: str | None = Form(default=None),
):
    # Support both JSON body (legacy) and multipart form with an uploaded
    # speaker file. Form fields override JSON body when provided.
    body = payload or {}
    text = str(text or body.get("text", ""))

    # Determine speaker path: prefer uploaded file, then form value, then JSON.
    tmp_speaker_path = None
    speaker = body.get("speaker_wav") or body.get("speaker")
    if speaker_file is not None:
        import tempfile

        suffix = Path(speaker_file.filename).suffix or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_speaker_path = tmp.name
            content = await speaker_file.read()
            tmp.write(content)

    speaker_path = tmp_speaker_path or speaker

    result, audio_bytes = synthesize(text, speaker_wav=speaker_path, language=language)
    if not result.get("ok"):
        status = result.get("status", 500)
        status_code = int(status) if isinstance(status, (int, str)) else 500
        return JSONResponse(
            {"error": str(result["message"])},
            status_code=status_code,
        )

    return Response(content=audio_bytes, media_type=str(result["mime_type"]))

    # cleanup uploaded temporary file if created
    try:
        if tmp_speaker_path:
            Path(tmp_speaker_path).unlink(missing_ok=True)
    except Exception:
        pass


app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
