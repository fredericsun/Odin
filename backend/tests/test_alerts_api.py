from fastapi.testclient import TestClient
from sqlmodel import Session

from app.db import get_engine, init_db
from app.main import create_app
from app.models import Alert


def test_alerts_endpoint_reads_db(monkeypatch, tmp_path):
    db_path = tmp_path / "alerts.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    engine = get_engine()
    init_db(engine)
    with Session(engine) as session:
        session.add(Alert(asset_id="t1", subject="S", body="B"))
        session.commit()

    app = create_app()
    client = TestClient(app)
    resp = client.get("/api/alerts")
    assert resp.status_code == 200
    assert resp.json()[0]["asset_id"] == "t1"
