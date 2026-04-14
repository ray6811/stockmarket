# Stock Analysis Microservices (scaffold)

This workspace contains a microservices-based scaffold for a stock market analysis system. It includes examples and working implementations for several core services built with FastAPI.

Services included (examples):
- `signal-engine-service` (FastAPI) — computes BUY/SELL/HOLD signals
- `indicator-service` (FastAPI) — computes RSI, MA, MACD
- `price-action-service` (FastAPI) — support/resistance, patterns, breakout
- `backtesting-service` (FastAPI) — runs a simple backtest
- `notification-service` (FastAPI) — sends Telegram alerts

Run locally with Docker Compose:

```bash
docker-compose build
docker-compose up
```

Each service exposes a port per the `docker-compose.yml`.

Auth removed for this development build: frontend opens directly to the dashboard.


See `k8s/` for example Kubernetes manifests for `signal-engine-service`.
