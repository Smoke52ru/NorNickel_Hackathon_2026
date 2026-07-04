"""Точка входа FastAPI для Vercel.

dev  — MOCK=1, готовые ответы без данных/LLM.
master — MOCK=0, реальный RAG (data/vercel/, LLM и эмбеддинги через API).
"""
import os

_branch = os.environ.get("VERCEL_GIT_COMMIT_REF", "")
if _branch == "master":
    os.environ.setdefault("MOCK", "0")
    os.environ.setdefault("EMBEDDER", "yandex")
    os.environ.setdefault("DATA_PROCESSED", "data/vercel")
else:
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
    return {
        "service": "nauchny-klubok",
        "branch": _branch or None,
        "mock": os.environ.get("MOCK", "1") != "0",
    }
