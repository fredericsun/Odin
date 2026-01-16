from app.services.signal_engine import RingBuffer, SignalEngine


def test_odds_jump_detected():
    buffer = RingBuffer(maxlen=5)
    engine = SignalEngine(odds_jump_abs=0.10)

    for price in [0.40, 0.41, 0.42, 0.43]:
        buffer.append({"odds": price, "volume": 100, "liquidity": 500})

    event = engine.detect(buffer, {"odds": 0.55, "volume": 110, "liquidity": 520})
    assert event is not None
    assert event["triggered"] == ["odds_jump_abs"]
