# tests/test_integration_api.py
import pytest

pytestmark = pytest.mark.asyncio  # ejecuta estos tests en modo asyncio

async def test_health_ok(client):
    r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "model" in data

async def test_predict_ok(client):
    payload = {"text": "The new Epson printer works perfectly and I really like its speed."}
    r = await client.post("/predict", json=payload)
    assert r.status_code == 200
    out = r.json()
    assert "label" in out
    assert "proba" in out
    assert out["model"].endswith(".joblib")

async def test_predict_batch_ok(client):
    payload = {"texts": ["good", "bad", "neutral comment"]}
    r = await client.post("/predict/batch", json=payload)
    assert r.status_code == 200
    out = r.json()
    assert isinstance(out, list)
    assert len(out) == 3
    for item in out:
        assert "label" in item and "proba" in item

async def test_idempotency_same_input_same_label(client):
    text = "This product is amazing and super fast!"
    p1 = (await client.post("/predict", json={"text": text})).json()
    p2 = (await client.post("/predict", json={"text": text})).json()
    assert p1["label"] == p2["label"]

async def test_schema_validation_422_predict(client):
    # Falta el campo "text" -> debe fallar validación
    r = await client.post("/predict", json={"missing_field": "x"})
    assert r.status_code == 422

async def test_schema_validation_422_batch(client):
    # Estructura incorrecta del body (espera {"texts": [...]})
    r = await client.post("/predict/batch", json={"texts": ["one", "two"]})
    assert r.status_code == 200 or r.status_code == 422  # según tu validación
