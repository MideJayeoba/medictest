import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app import app


class AppApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_assistant_respond_rejects_empty_input(self):
        response = self.client.post("/api/assistant/respond", json={"input": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("required", response.json()["error"].lower())

    def test_assistant_respond_returns_reply_payload(self):
        with patch("backend.app.get_bio_mistral_response", return_value="Try resting and staying hydrated."):
            response = self.client.post(
                "/api/assistant/respond",
                json={"input": "I have mild fever and sore throat"},
            )
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["model"], "BioMistral")
        self.assertIsInstance(body["reply"], str)
        self.assertGreater(len(body["reply"]), 0)


if __name__ == "__main__":
    unittest.main()
