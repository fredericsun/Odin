import feedparser


def fetch_rss(urls: list[str]) -> list[dict]:
    items = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            items.append({"title": entry.title, "url": entry.link})
    return items
