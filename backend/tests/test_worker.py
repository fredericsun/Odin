from sqlmodel import Session, select

from app.db import get_engine, init_db
from app.models import Explanation, InstrumentMapping, MarketEvent
from app.services.clob_ws_client import ClobWsClient
from app.services.gamma_client import GammaClient
from app.worker import run_once


class FakeSources:
    def __init__(self):
        self.called = False

    def __call__(self):
        self.called = True
        return [{"title": "T", "url": "https://example.com"}]


class FakeLLM:
    def summarize(self, prompt: str) -> str:
        return "Summary"


def test_worker_persists_enrichment(monkeypatch, tmp_path):
    db_path = tmp_path / "worker.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    engine = get_engine()
    init_db(engine)

    def fake_fetch_markets(self, limit=50):
        return [{"id": "m1", "liquidity": 10, "clobTokenIds": ["t1"]}]

    class FakeWebSocket:
        def close(self):
            return None

    def fake_connect(self):
        return FakeWebSocket()

    def fake_subscribe(self, ws, asset_ids):
        ws.asset_ids = asset_ids

    def fake_iter_messages(self, ws, max_messages=None):
        yield {
            "odds": 0.1,
            "asset_id": "t1",
            "market_id": "m1",
            "question": "Will BTC be above $100k?",
        }
        yield {
            "odds": 0.7,
            "asset_id": "t1",
            "market_id": "m1",
            "question": "Will BTC be above $100k?",
        }

    monkeypatch.setattr(GammaClient, "fetch_markets", fake_fetch_markets)
    monkeypatch.setattr(ClobWsClient, "connect", fake_connect)
    monkeypatch.setattr(ClobWsClient, "subscribe", fake_subscribe)
    monkeypatch.setattr(ClobWsClient, "iter_market_messages", fake_iter_messages)

    fake_sources = FakeSources()
    result = run_once(
        engine=engine,
        max_messages=2,
        llm_client=FakeLLM(),
        sources=fake_sources(),
    )
    assert result["events_count"] == 1

    with Session(engine) as session:
        explanation = session.exec(select(Explanation)).first()
        assert explanation.summary == "Summary"
        assert session.exec(select(InstrumentMapping)).all()
        event = session.exec(select(MarketEvent)).first()
        assert event.score > 0


def test_worker_uses_default_sources(monkeypatch, tmp_path):
    db_path = tmp_path / "worker-default.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    engine = get_engine()
    init_db(engine)

    def fake_fetch_markets(self, limit=50):
        return [{"id": "m1", "liquidity": 10, "clobTokenIds": ["t1"]}]

    class FakeWebSocket:
        def close(self):
            return None

    def fake_connect(self):
        return FakeWebSocket()

    def fake_subscribe(self, ws, asset_ids):
        ws.asset_ids = asset_ids

    def fake_iter_messages(self, ws, max_messages=None):
        yield {
            "odds": 0.1,
            "asset_id": "t1",
            "market_id": "m1",
            "question": "Will BTC be above $100k?",
        }
        yield {
            "odds": 0.5,
            "asset_id": "t1",
            "market_id": "m1",
            "question": "Will BTC be above $100k?",
        }

    fake_sources = FakeSources()

    monkeypatch.setattr(GammaClient, "fetch_markets", fake_fetch_markets)
    monkeypatch.setattr(ClobWsClient, "connect", fake_connect)
    monkeypatch.setattr(ClobWsClient, "subscribe", fake_subscribe)
    monkeypatch.setattr(ClobWsClient, "iter_market_messages", fake_iter_messages)
    monkeypatch.setattr(
        "app.worker.fetch_default_sources", fake_sources, raising=False
    )

    run_once(engine=engine, max_messages=2, llm_client=FakeLLM())
    assert fake_sources.called is True


def test_worker_skips_llm_without_api_key(monkeypatch, tmp_path):
    db_path = tmp_path / "worker-nokey.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    engine = get_engine()
    init_db(engine)

    def fake_fetch_markets(self, limit=50):
        return [{"id": "m1", "liquidity": 10, "clobTokenIds": ["t1"]}]

    class FakeWebSocket:
        def close(self):
            return None

    def fake_connect(self):
        return FakeWebSocket()

    def fake_subscribe(self, ws, asset_ids):
        ws.asset_ids = asset_ids

    def fake_iter_messages(self, ws, max_messages=None):
        yield {
            "odds": 0.1,
            "asset_id": "t1",
            "market_id": "m1",
            "question": "Will BTC be above $100k?",
        }
        yield {
            "odds": 0.5,
            "asset_id": "t1",
            "market_id": "m1",
            "question": "Will BTC be above $100k?",
        }

    monkeypatch.setattr(GammaClient, "fetch_markets", fake_fetch_markets)
    monkeypatch.setattr(ClobWsClient, "connect", fake_connect)
    monkeypatch.setattr(ClobWsClient, "subscribe", fake_subscribe)
    monkeypatch.setattr(ClobWsClient, "iter_market_messages", fake_iter_messages)

    run_once(engine=engine, max_messages=2)

    with Session(engine) as session:
        explanation = session.exec(select(Explanation)).first()
        assert explanation.confidence == 0.0
