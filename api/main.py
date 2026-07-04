import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core import config, rag
from core.embeddings import get_embedder
from core.graph_store import NetworkxGraphStore
from core.llm import get_llm
from core.retrieval import HybridRetriever

app = FastAPI(title="Научный клубок — API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def _load():
    """Артефакты сборки грузим один раз при старте: граф, поисковый индекс и документы.
    Если сборки не было - API поднимется и честно ответит, что база пуста."""
    graph_path = os.path.join(config.DATA_PROCESSED, "graph.pkl")
    docs_path = os.path.join(config.DATA_PROCESSED, "documents.jsonl")
    graph = NetworkxGraphStore().load(graph_path) if os.path.exists(graph_path) else None
    try:
        embedder = get_embedder()
    except Exception:
        embedder = None  # эмбеддер недоступен - поиск деградирует до BM25
    retriever = HybridRetriever.from_processed(config.DATA_PROCESSED, embedder=embedder)
    docs = {}
    if os.path.exists(docs_path):
        with open(docs_path, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                docs[d["doc_id"]] = d
    return graph, retriever, docs


if config.MOCK:
    # фронт-режим: ничего тяжёлого не грузим, эндпоинты отдают готовые ответы
    GRAPH = RETRIEVER = DOCS = LLM = None
else:
    GRAPH, RETRIEVER, DOCS = _load()
    LLM = get_llm()


class NumericFilter(BaseModel):
    property: str
    op: str = "<="                        # < <= > >= =
    value: float


class Filters(BaseModel):
    geo: str | None = None                # "ru" | "foreign"
    year_from: int | None = None
    year_to: int | None = None
    types: list[str] | None = None        # Material, Process, Equipment, Property, ...
    numeric: NumericFilter | None = None   # напр. {"property":"сульфаты","op":"<","value":200}


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    filters: Filters | None = None


class CompareRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


@app.get("/health")
def health():
    return {"status": "ok", "mock": config.MOCK,
            "graph": GRAPH.stats() if GRAPH else None,
            "documents": len(DOCS) if DOCS else 0}


@app.post("/ask")
def ask(req: AskRequest):
    if config.MOCK:
        from core import mock
        return mock.ASK
    if RETRIEVER is None:
        return {"answer": "База знаний не собрана. Запусти parse и build.",
                "answer_links": [], "sources": [], "confidence": "low",
                "graph": {"nodes": [], "edges": []}, "gaps": [], "contradictions": []}
    try:
        return rag.answer(req.question, RETRIEVER, GRAPH, LLM,
                          filters=req.filters.model_dump() if req.filters else None)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ошибка генерации ответа: {e}")


@app.post("/compare")
def compare(req: CompareRequest):
    """Сравнительная таблица источников по теме (год, гео, числа, вырезка)."""
    if config.MOCK:
        from core import mock
        return mock.COMPARE
    if RETRIEVER is None:
        return {"question": req.question, "rows": []}
    return rag.compare(req.question, RETRIEVER, GRAPH)


@app.get("/document/{doc_id}")
def document(doc_id: str):
    """Полный текст и метаданные документа - для перехода из источников и узлов Publication."""
    if config.MOCK:
        from core import mock
        return mock.DOC
    d = DOCS.get(doc_id)
    if not d:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return {"doc_id": d["doc_id"], "title": d.get("title", ""), "year": d.get("year"),
            "lang": d.get("lang"), "source_path": d.get("source_path"), "text": d.get("text", "")}


@app.get("/graph")
def graph_overview(limit: int = 150):
    """Обзорная «карта знаний»: самые связанные узлы всего графа."""
    if config.MOCK:
        from core import mock
        return mock.GRAPH
    if GRAPH is None:
        return {"nodes": [], "edges": []}
    return GRAPH.overview(max_nodes=limit)
