const test = require("node:test");
const assert = require("node:assert/strict");
const request = require("supertest");
const app = require("../backend/src/app");

test("GET /api/health returns status ok", async () => {
  const response = await request(app).get("/api/health");
  assert.equal(response.status, 200);
  assert.equal(response.body.status, "ok");
});

test("POST /api/assistant/respond validates empty input", async () => {
  const response = await request(app).post("/api/assistant/respond").send({ input: "" });
  assert.equal(response.status, 400);
  assert.match(response.body.error, /required/i);
});

test("POST /api/assistant/respond returns reply payload", async () => {
  const response = await request(app)
    .post("/api/assistant/respond")
    .send({ input: "I have mild fever and sore throat" });

  assert.equal(response.status, 200);
  assert.equal(response.body.model, "BioMistral");
  assert.equal(typeof response.body.reply, "string");
  assert.ok(response.body.reply.length > 0);
});
