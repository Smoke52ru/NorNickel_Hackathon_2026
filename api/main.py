from typing import Literal, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Научный клубок — API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class SearchFilters(BaseModel):
    node_types: list[str] = Field(default_factory=list, alias="nodeTypes")
    geography: Literal["all", "domestic", "foreign"] = "all"
    year_from: Optional[int] = Field(default=None, alias="yearFrom")
    year_to: Optional[int] = Field(default=None, alias="yearTo")
    min_confidence: Literal["high", "medium", "low"] = Field(default="low", alias="minConfidence")
    material_keyword: str = Field(default="", alias="materialKeyword")
    process_keyword: str = Field(default="", alias="processKeyword")
    show_contradictions: bool = Field(default=True, alias="showContradictions")
    show_gaps: bool = Field(default=True, alias="showGaps")

    model_config = {"populate_by_name": True}


class AskRequest(BaseModel):
    question: str
    filters: Optional[SearchFilters] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest):
    answer = (
        f"По запросу «{req.question}»: для обессоливания шахтных вод "
        "применяются обратный осмос и ионный обмен. "
        "При электроэкстракции никеля описаны решения циркуляции католита."
    )
    # TODO: заменить мок на core.rag.answer(...)
    return {
        "answer": answer,
        "answer_links": [
            {"nodeId": "n2", "start": answer.index("обратный осмос"), "end": answer.index("обратный осмос") + len("обратный осмос")},
            {"nodeId": "n3", "start": answer.index("ионный обмен"), "end": answer.index("ионный обмен") + len("ионный обмен")},
            {"nodeId": "n4", "start": answer.index("электроэкстракции никеля"), "end": answer.index("электроэкстракции никеля") + len("электроэкстракции никеля")},
        ],
        "sources": [
            {
                "doc_id": "obzor_ochistka_vod",
                "title": "Методы очистки шахтных вод",
                "year": 2021,
                "snippet": "Обратный осмос применяется при сульфатах…",
            },
        ],
        "confidence": "medium",
        "graph": {
            "nodes": [
                {"id": "n1", "label": "Шахтные воды", "type": "Material"},
                {"id": "n2", "label": "Обратный осмос", "type": "Process"},
                {"id": "n3", "label": "Ионный обмен", "type": "Process"},
                {"id": "n4", "label": "Электроэкстракция", "type": "Process"},
                {"id": "n5", "label": "Сухой остаток ≤1000 мг/дм³", "type": "Property"},
            ],
            "edges": [
                {"from": "n2", "to": "n1", "label": "uses_material", "flag": "normal"},
                {"from": "n2", "to": "n5", "label": "produces_output", "flag": "normal"},
                {"from": "n3", "to": "n1", "label": "uses_material", "flag": "normal"},
                {"from": "n4", "to": "n1", "label": "uses_material", "flag": "normal"},
            ],
        },
        "gaps": ["нет данных: холодный климат + кучное выщелачивание + никелевая руда"],
        "contradictions": [
            {
                "about": "оптимальная скорость циркуляции католита",
                "sources": ["obzor_electro_ni", "statya_2024"],
            },
        ],
        "filters_applied": req.filters.model_dump(by_alias=True) if req.filters else None,
    }
