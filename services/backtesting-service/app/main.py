import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backtesting_service")

app = FastAPI(title="Backtesting Service")


class Candle(BaseModel):
    t: int
    o: float
    h: float
    l: float
    c: float
    v: float


class BacktestRequest(BaseModel):
    candles: List[Candle]


@app.post('/backtest')
async def backtest(req: BacktestRequest):
    try:
        df = pd.DataFrame([c.dict() for c in req.candles])
        if df.empty:
            raise ValueError('empty data')

        # Simplified strategy: use RSI + MA + price-action rules
        close = df['c']
        # compute indicators
        ma50 = close.rolling(window=50, min_periods=1).mean()
        delta = close.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ma_up = up.ewm(alpha=1/14, adjust=False).mean()
        ma_down = down.ewm(alpha=1/14, adjust=False).mean()
        rs = ma_up / (ma_down.replace(0, 1e-8))
        rsi = 100 - (100 / (1 + rs))

        cash = 10000.0
        pos = 0
        entry_price = 0
        trades = []

        for i in range(1, len(df)):
            price = float(close.iloc[i])
            support = float(df['l'].iloc[max(0, i-20):i].min())
            resistance = float(df['h'].iloc[max(0, i-20):i].max())
            ma = float(ma50.iloc[i])
            r = float(rsi.iloc[i])

            # Buy
            if (abs(price - support) / support * 100 <= 2) and r < 35 and price > ma and pos == 0:
                # buy as much as possible
                qty = cash // price
                if qty > 0:
                    pos = qty
                    entry_price = price
                    cash -= qty * price
                    trades.append({'type': 'buy', 'price': price, 'qty': qty, 'idx': i})
            # Sell
            elif (abs(price - resistance) / resistance * 100 <= 2) and r > 65 and price < ma and pos > 0:
                cash += pos * price
                trades.append({'type': 'sell', 'price': price, 'qty': pos, 'idx': i})
                pos = 0

        # close positions at last price
        if pos > 0:
            cash += pos * float(close.iloc[-1])
            trades.append({'type': 'sell', 'price': float(close.iloc[-1]), 'qty': pos, 'idx': len(df)-1})
            pos = 0

        profit = cash - 10000.0
        num_trades = len([t for t in trades if t['type'] == 'buy'])
        wins = 0
        # naive accuracy: count profitable round-trip trades
        for i in range(0, len(trades)-1, 2):
            b = trades[i]
            s = trades[i+1] if i+1 < len(trades) else None
            if s and s['price'] > b['price']:
                wins += 1

        accuracy = (wins / num_trades * 100) if num_trades > 0 else 0.0

        # max drawdown (naive)
        equity = [10000.0]
        cash2 = 10000.0
        pos2 = 0
        for i in range(len(df)):
            price = float(close.iloc[i])
            equity.append(cash2 + pos2 * price)
        equity = np.array(equity)
        peak = np.maximum.accumulate(equity)
        drawdown = np.max((peak - equity) / peak) if len(equity) > 0 else 0.0

        return {"profit": round(profit, 2), "accuracy": round(accuracy, 2), "drawdown": round(float(drawdown), 4), "trades": num_trades, "report": {"trades": trades}}
    except Exception as e:
        logger.exception('Backtest failed')
        raise HTTPException(status_code=500, detail=str(e))
