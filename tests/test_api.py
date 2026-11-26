import pytest
from fastapi.testclient import TestClient

from backend.main import app

# Adjust to match the real backend
HEALTH_URL = "/health"
PREDICT_URL = "/predict"
FIELD = "text"

CATEGORIES = {"application", "complaint", "invoice", "contract", "request", "correspondence"}


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    assert client.get(HEALTH_URL).status_code == 200


def test_valid_text(client):
    r = client.post(PREDICT_URL, json={FIELD: "Please find attached the invoice for March. Total due: 500 USD."})
    assert r.status_code == 200
    body = r.json()
    assert body["predicted_category"].lower() in CATEGORIES
    assert 0 <= body["confidence"] <= 1  # assumes a 0-1 scale
    assert body["routing_department"]


@pytest.mark.parametrize("payload", [{}, {FIELD: ""}, {FIELD: "   "}, {FIELD: None}, {FIELD: 123}])
def test_invalid_input(client, payload):
    r = client.post(PREDICT_URL, json=payload)
    assert r.status_code in (400, 422)
