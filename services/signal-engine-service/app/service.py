import logging
from typing import Dict


logger = logging.getLogger("signal_engine")


def pct_distance(a: float, b: float) -> float:
    if b == 0:
        return 100.0
    return abs(a - b) / b * 100.0


def generate_signal(payload: Dict) -> Dict:
    try:
        price = float(payload.get("price"))
        rsi = float(payload.get("rsi"))
        ma50 = float(payload.get("ma50"))
        support = float(payload.get("support"))
        resistance = float(payload.get("resistance"))
        volume = payload.get("volume")
        avg_volume = payload.get("avg_volume")

        near_support = pct_distance(price, support) <= 2.0
        near_resistance = pct_distance(price, resistance) <= 2.0
        above_ma = price > ma50
        below_ma = price < ma50

        reason_parts = []
        score = 50.0

        if near_support:
            reason_parts.append("price near support")
            score += 15
        if near_resistance:
            reason_parts.append("price near resistance")
            score -= 15
        if rsi < 35:
            reason_parts.append("RSI oversold")
            score += 20
        if rsi > 65:
            reason_parts.append("RSI overbought")
            score -= 20
        if above_ma:
            reason_parts.append("price above MA50")
            score += 10
        if below_ma:
            reason_parts.append("price below MA50")
            score -= 10

        signal = "HOLD"

        # Strong signals
        if resistance and price > resistance and avg_volume and volume and volume > avg_volume * 1.5:
            signal = "STRONG BUY"
            reason_parts.insert(0, "breakout above resistance with high volume")
            score = min(100.0, score + 20)
        elif support and price < support:
            signal = "STRONG SELL"
            reason_parts.insert(0, "breakdown below support")
            score = min(100.0, score + 20)
        else:
            # Regular buy/sell
            if near_support and rsi < 35 and above_ma:
                signal = "BUY"
            elif near_resistance and rsi > 65 and below_ma:
                signal = "SELL"
            else:
                signal = "HOLD"

        score = max(0.0, min(100.0, score))
        reason = ", ".join(reason_parts) if reason_parts else "no strong confirming signals"

        return {"signal": signal, "confidence": round(score, 2), "reason": reason}
    except Exception as e:
        logger.exception("Error generating signal")
        raise
