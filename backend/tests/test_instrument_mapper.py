from app.services.instrument_mapper import map_instruments


def test_map_instruments_matches_symbol():
    event = {"question": "Will BTC be above $100k?"}
    mappings = map_instruments(event)
    assert {"type": "crypto", "symbol": "BTC-USD"} in mappings
