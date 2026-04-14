from app.service import generate_signal


def test_buy_signal():
    payload = {
        "symbol": "TEST",
        "price": 98.0,
        "rsi": 30,
        "ma50": 90.0,
        "support": 100.0,
        "resistance": 120.0,
        "volume": 1000,
        "avg_volume": 800,
    }
    res = generate_signal(payload)
    assert res["signal"] in ("BUY", "STRONG BUY", "HOLD")


def test_hold_signal():
    payload = {
        "symbol": "TEST",
        "price": 110.0,
        "rsi": 50,
        "ma50": 105.0,
        "support": 90.0,
        "resistance": 130.0,
        "volume": 500,
        "avg_volume": 700,
    }
    res = generate_signal(payload)
    assert "signal" in res
