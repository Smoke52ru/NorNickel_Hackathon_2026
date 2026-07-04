from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Научный клубок — API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest):
    # TODO: заменить мок на core.rag.answer(...)
    return {
        "answer": f"[мок] Ответ на вопрос: «{req.question}».",
        "sources": [
            {"doc_id": "obzor_ochistka_vod", "title": "Методы очистки шахтных вод",
             "year": 2021, "snippet": "Обратный осмос применяется при сульфатах…"},
        ],
        "confidence": "medium",
        "graph": {
            "nodes": [
                {"id": "n1", "label": "Шахтные воды", "type": "Material"},
                {"id": "n2", "label": "Обратный осмос", "type": "Process"},
                {"id": "n3", "label": "Сухой остаток ≤1000 мг/дм³", "type": "Property"},
            ],
            "edges": [
                {"from": "n2", "to": "n1", "label": "uses_material", "flag": "normal"},
                {"from": "n2", "to": "n3", "label": "produces_output", "flag": "normal"},
            ],
        },
        "gaps": ["нет данных: холодный климат + кучное выщелачивание + никелевая руда"],
        "contradictions": [
            {"about": "оптимальная скорость циркуляции католита",
             "sources": ["obzor_electro_ni", "statya_2024"]},
        ],
    }
