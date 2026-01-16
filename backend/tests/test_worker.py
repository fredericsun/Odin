from app.worker import run_once


def test_run_once_returns_result():
    result = run_once()
    assert result["status"] == "ok"
