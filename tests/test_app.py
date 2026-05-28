import unittest

from backend.app import app


class AppApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_assistant_respond_rejects_empty_input(self):
        response = self.client.post("/api/assistant/respond", json={"input": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("required", response.get_json()["error"].lower())

    def test_assistant_respond_returns_reply_payload(self):
        response = self.client.post(
            "/api/assistant/respond",
            json={"input": "I have mild fever and sore throat"},
        )
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["model"], "BioMistral")
        self.assertIsInstance(body["reply"], str)
        self.assertGreater(len(body["reply"]), 0)


if __name__ == "__main__":
    unittest.main()
