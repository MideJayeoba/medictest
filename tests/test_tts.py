import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app import app


class TtsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_tts_endpoint_returns_audio(self):
        fake_audio = b"RIFF....WAVEfmt "

        with patch("backend.app.synthesize", return_value=({"ok": True, "status": 200, "mime_type": "audio/wav"}, fake_audio)):
            response = self.client.post(
                "/api/tts",
                json={"text": "Hello world", "speaker_wav": "/path/to/speaker.wav", "language": "en"},
            )

        self.assertEqual(response.status_code, 200)
        # content-type header for FastAPI Response will include the mime type
        self.assertIn("audio/wav", response.headers.get("content-type", ""))
        self.assertEqual(response.content, fake_audio)

    def test_tts_endpoint_accepts_uploaded_speaker(self):
        fake_audio = b"RIFF....WAVEfmt "
        # create an in-memory bytes file representing a speaker wav
        speaker_bytes = b"RIFFfakewavdata"

        with patch("backend.app.synthesize", return_value=({"ok": True, "status": 200, "mime_type": "audio/wav"}, fake_audio)):
            files = {"speaker_file": ("speaker.wav", speaker_bytes, "audio/wav")}
            data = {"text": "Hello with upload", "language": "en"}
            response = self.client.post("/api/tts", files=files, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, fake_audio)


if __name__ == "__main__":
    unittest.main()
