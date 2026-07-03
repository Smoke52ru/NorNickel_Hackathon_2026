import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core import config, rag
from core.graph_store import NetworkxGraphStore
from core.llm import get_llm
from core.retrieval import BM25Retriever

app = FastAPI(title="Научный клубок — API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def _load():
    graph_path = os.path.join(config.DATA_PROCESSED, "graph.pkl")
    docs_path = os.path.join(config.DATA_PROCESSED, "documents.jsonl")
    graph = NetworkxGraphStore().load(graph_path) if os.path.exists(graph_path) else None
    retriever = BM25Retriever.from_jsonl(docs_path) if os.path.exists(docs_path) else None
    return graph, retriever


GRAPH, RETRIEVER = _load()
LLM = get_llm()


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok", "graph": GRAPH.stats() if GRAPH else None,
            "retriever": bool(RETRIEVER)}


@app.post("/ask")
def ask(req: AskRequest):
    if RETRIEVER is None:
        return {"answer": "База знаний не собрана. Запусти parse и build (см. README).",
                "sources": [], "confidence": "low",
                "graph": {"nodes": [], "edges": []}, "gaps": [], "contradictions": []}
    return rag.answer(req.question, RETRIEVER, GRAPH, LLM)
