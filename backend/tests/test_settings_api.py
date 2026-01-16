from fastapi.testclient import TestClient

from app.main import create_app


def test_get_and_update_settings(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    app = create_app()
    client = TestClient(app)

    resp = client.get("/api/settings")
    assert resp.status_code == 200
    data = resp.json()
    assert data["market_scope"] == "top_50_liquidity"

    resp = client.post("/api/settings", json={"max_position_usd": 250})
    assert resp.status_code == 200
    assert resp.json()["max_position_usd"] == 250
