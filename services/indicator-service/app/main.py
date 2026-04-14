import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("indicator_service")

app = FastAPI(title="Indicator Service")


class Candle(BaseModel):
    t: int
    o: float
    h: float
    l: float
    c: float
    v: float


class IndicatorRequest(BaseModel):
    candles: List[Candle]


@app.post("/indicators")
async def indicators(req: IndicatorRequest):
    try:
        df = pd.DataFrame([c.dict() for c in req.candles])
        close = df["c"]

        # MA
        ma50 = close.rolling(window=50, min_periods=1).mean().iloc[-1]
        ma200 = close.rolling(window=200, min_periods=1).mean().iloc[-1]

        # RSI 14
        delta = close.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ma_up = up.ewm(alpha=1/14, adjust=False).mean()
        ma_down = down.ewm(alpha=1/14, adjust=False).mean()
        rs = ma_up / (ma_down.replace(0, 1e-8))
        rsi = 100 - (100 / (1 + rs)).iloc[-1]

        # MACD
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd = (ema12 - ema26).iloc[-1]

        return {"rsi": float(round(rsi, 4)), "ma50": float(round(ma50, 4)), "ma200": float(round(ma200, 4)), "macd": float(round(macd, 6))}
    except Exception as e:
        logger.exception("Indicator calculation failed")
        raise HTTPException(status_code=500, detail=str(e))
