import feedparser

from app.services.source_registry import DEFAULT_RSS_SOURCES


def fetch_rss(urls: list[str]) -> list[dict]:
    items = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            items.append({"title": entry.title, "url": entry.link})
    return items


def fetch_default_sources() -> list[dict]:
    return fetch_rss(DEFAULT_RSS_SOURCES)
