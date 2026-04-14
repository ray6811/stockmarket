import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import SignalRequest, SignalResponse
from .service import generate_signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("signal_engine_app")

app = FastAPI(title="Signal Engine Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/signal", response_model=SignalResponse)
async def signal(req: SignalRequest):
    try:
        payload = req.dict()
        result = generate_signal(payload)
        return result
    except Exception as e:
        logger.exception("Failed to compute signal")
        raise HTTPException(status_code=500, detail=str(e))
