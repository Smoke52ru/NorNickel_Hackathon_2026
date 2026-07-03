import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core import config, rag
from core.graph_store import NetworkxGraphStore
from core.llm import get_llm
from core.retrieval import BM25Retriever

app = FastAPI(title="Научный клубок — API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def _load():
    """Грузим артефакты сборки один раз при старте: граф, поисковый индекс
    и документы (для /document). Если сборки не было — API поднимется, но честно
    ответит, что база знаний пуста."""
    graph_path = os.path.join(config.DATA_PROCESSED, "graph.pkl")
    docs_path = os.path.join(config.DATA_PROCESSED, "documents.jsonl")
    graph = NetworkxGraphStore().load(graph_path) if os.path.exists(graph_path) else None
    retriever, docs = None, {}
    if os.path.exists(docs_path):
        retriever = BM25Retriever.from_jsonl(docs_path)
        with open(docs_path, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                docs[d["doc_id"]] = d
    return graph, retriever, docs


GRAPH, RETRIEVER, DOCS = _load()
LLM = get_llm()


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


@app.get("/health")
def health():
    return {"status": "ok", "graph": GRAPH.stats() if GRAPH else None,
            "documents": len(DOCS)}


@app.post("/ask")
def ask(req: AskRequest):
    if RETRIEVER is None:
        return {"answer": "База знаний не собрана. Запусти parse и build (см. README).",
                "sources": [], "confidence": "low",
                "graph": {"nodes": [], "edges": []}, "gaps": [], "contradictions": []}
    try:
        return rag.answer(req.question, RETRIEVER, GRAPH, LLM)
    except Exception as e:
        # чаще всего это недоступность LLM-API; фронту достаточно кода и краткого текста
        raise HTTPException(status_code=502, detail=f"Ошибка генерации ответа: {e}")


@app.get("/document/{doc_id}")
def document(doc_id: str):
    """Полный текст и метаданные документа — для перехода из источников и узлов Publication."""
    d = DOCS.get(doc_id)
    if not d:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return {"doc_id": d["doc_id"], "title": d.get("title", ""), "year": d.get("year"),
            "lang": d.get("lang"), "source_path": d.get("source_path"), "text": d.get("text", "")}


@app.get("/graph")
def graph_overview(limit: int = 150):
    """Обзорная «карта знаний»: самые связанные узлы всего графа."""
    if GRAPH is None:
        return {"nodes": [], "edges": []}
    return GRAPH.overview(max_nodes=limit)
