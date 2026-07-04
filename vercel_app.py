"""Точка входа FastAPI для Vercel.

На serverless по умолчанию MOCK=1 — без torch, FAISS и data/processed/.
Маршруты api.main доступны с префиксом /api (как в dev-прокси Vite).
"""
import os

os.environ.setdefault("MOCK", "1")

from fastapi import FastAPI  # noqa: E402

from api.main import app as api_app  # noqa: E402

app = FastAPI(
    title="Научный клубок — Vercel",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
app.mount("/api", api_app)


@app.get("/")
def root():
    return {"service": "nauchny-klubok", "mock": os.environ.get("MOCK", "1") != "0"}
