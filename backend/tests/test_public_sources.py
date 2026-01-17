import feedparser

from app.services.public_sources import fetch_default_sources


def test_fetch_default_sources(monkeypatch):
    class FakeFeed:
        entries = [type("Entry", (), {"title": "T", "link": "L"})()]

    def fake_parse(url):
        return FakeFeed()

    monkeypatch.setattr(feedparser, "parse", fake_parse)
    items = fetch_default_sources()
    assert len(items) > 0
    assert items[0] == {"title": "T", "url": "L"}
