from pydantic import BaseModel
from typing import Optional, List


class Candle(BaseModel):
    t: int
    o: float
    h: float
    l: float
    c: float
    v: float


class SignalRequest(BaseModel):
    symbol: str
    price: float
    rsi: float
    ma50: float
    support: float
    resistance: float
    volume: Optional[float] = None
    avg_volume: Optional[float] = None


class SignalResponse(BaseModel):
    signal: str
    confidence: float
    reason: str
