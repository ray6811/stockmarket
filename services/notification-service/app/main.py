import os
import logging
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification_service")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = FastAPI(title="Notification Service")


class NotifyRequest(BaseModel):
    stock: str
    signal: str
    confidence: float = 0.0


@app.post('/notify')
async def notify(req: NotifyRequest):
    try:
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            raise HTTPException(status_code=500, detail="TELEGRAM_TOKEN or TELEGRAM_CHAT_ID not configured")

        text = f"Signal for {req.stock}: {req.signal} (confidence={req.confidence})"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        resp = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text})
        if resp.status_code != 200:
            logger.error("Telegram send failed: %s", resp.text)
            raise HTTPException(status_code=500, detail="telegram send failed")

        return {"status": "sent"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception('Notification failed')
        raise HTTPException(status_code=500, detail=str(e))
