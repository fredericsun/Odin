from app.services.source_registry import DEFAULT_RSS_SOURCES


def test_default_sources_include_crypto_and_general():
    assert any("reuters" in url for url in DEFAULT_RSS_SOURCES)
    assert any("coindesk" in url for url in DEFAULT_RSS_SOURCES)
