import pytest
from fastapi.testclient import TestClient

from backend.main import app


class FakePipeline:
    def __init__(self):
        self.predicted_text = None
        self.confidence_text = None

    def predict(self, texts):
        self.predicted_text = texts[0]
        return ["tech"]

    def predict_proba(self, texts):
        self.confidence_text = texts[0]
        return [[0.15, 0.85]]


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr("backend.main.joblib.load", lambda _: FakePipeline())
    monkeypatch.setattr("backend.main.preprocess_text", lambda text: f"processed: {text}")
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_classifies_text_and_returns_department(client):
    text = "Build a new product feature"
    response = client.post("/classify", json={"text": text})
    assert response.status_code == 200
    assert response.json() == {
        "label": "tech",
        "confidence": 0.85,
        "suggestion": "Engineering & Product Operations",
    }
    assert client.app.state.pipeline.predicted_text == f"processed: {text}"
    assert client.app.state.pipeline.confidence_text == f"processed: {text}"


@pytest.mark.parametrize(
    "payload",
    [{}, {"text": ""}, {"text": "   "}, {"text": None}, {"text": 123}, {"text": "x" * 250_001}],
)
def test_invalid_input(client, payload):
    response = client.post("/classify", json=payload)
    assert response.status_code == 422
