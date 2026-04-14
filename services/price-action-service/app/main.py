import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("price_action_service")

app = FastAPI(title="Price Action Service")


class Candle(BaseModel):
    t: int
    o: float
    h: float
    l: float
    c: float
    v: float


class PARequest(BaseModel):
    candles: List[Candle]


@app.post("/analyze")
async def analyze(req: PARequest):
    try:
        df = pd.DataFrame([c.dict() for c in req.candles])
        if df.empty:
            raise ValueError("empty candles")

        window = df.tail(20)
        support = float(window['l'].min())
        resistance = float(window['h'].max())

        # Candlestick patterns - check last two candles for engulfing
        pattern = "None"
        if len(df) >= 2:
            last = df.iloc[-1]
            prev = df.iloc[-2]
            # Bullish engulfing
            if prev['c'] < prev['o'] and last['c'] > last['o'] and last['c'] > prev['o'] and last['o'] < prev['c']:
                pattern = 'Bullish Engulfing'
            # Bearish engulfing
            if prev['c'] > prev['o'] and last['c'] < last['o'] and last['o'] > prev['c'] and last['c'] < prev['o']:
                pattern = 'Bearish Engulfing'

        # Pin bar detection: long wick
        last = df.iloc[-1]
        body = abs(last['c'] - last['o'])
        upper_wick = last['h'] - max(last['c'], last['o'])
        lower_wick = min(last['c'], last['o']) - last['l']
        if body < (last['h'] - last['l']) * 0.3:
            if lower_wick > body * 2:
                pattern = 'Pin Bar'
            if upper_wick > body * 2:
                pattern = 'Pin Bar'

        # Breakout
        latest_close = float(last['c'])
        avg_vol = float(window['v'].mean())
        breakout = False
        fake_breakout = False
        if latest_close > resistance:
            breakout = True
            # naive fake breakout: volume not supporting
            if last['v'] < avg_vol * 1.2:
                fake_breakout = True

        return {"support": support, "resistance": resistance, "pattern": pattern, "breakout": breakout, "fake_breakout": fake_breakout}
    except Exception as e:
        logger.exception("Price action analyze failed")
        raise HTTPException(status_code=500, detail=str(e))
