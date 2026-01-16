from fastapi.testclient import TestClient

from app.main import create_app


def test_reports_endpoint():
    app = create_app()
    client = TestClient(app)
    resp = client.get("/api/reports")
    assert resp.status_code == 200
    assert resp.json() == []
