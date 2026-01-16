from app.db import init_db, get_engine
from app.models import Settings


def test_init_db_creates_settings_row(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    engine = get_engine()
    init_db(engine)

    with engine.begin() as conn:
        result = conn.exec_driver_sql("select count(*) from settings")
        count = result.fetchone()[0]
    assert count == 1
