import os
import time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("auth_service")

SECRET = os.getenv("AUTH_SECRET", "devsecret")
ALGORITHM = "HS256"

app = FastAPI(title="Auth Service")

# Allow browser-based frontend to call this service.
# Use a permissive CORS policy for local development. Do NOT use `allow_credentials=True` with `allow_origins=["*"]`.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@app.post('/login', response_model=TokenResponse)
async def login(req: LoginRequest):
    # NOTE: this is a demo auth – replace with real user store in production
    if req.username == 'admin' and req.password == 'password':
        payload = {"sub": req.username, "iat": int(time.time())}
        token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail='invalid credentials')




class TokenRequest(BaseModel):
    token: str


@app.post('/verify')
async def verify(req: TokenRequest):
    try:
        data = jwt.decode(req.token, SECRET, algorithms=[ALGORITHM])
        return {"valid": True, "sub": data.get('sub')}
    except Exception as e:
        logger.exception('token verify failed')
        raise HTTPException(status_code=401, detail='invalid token')


@app.get('/health')
async def health():
    return {"status": "ok"}
