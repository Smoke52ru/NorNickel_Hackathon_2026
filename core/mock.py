"""Готовые ответы для MOCK-режима (config.MOCK=1): фронт разрабатывается без данных/LLM/torch.
Формат 1:1 совпадает с боевым — фронт потом переключается на реальный бэк без правок."""
import copy

from .linking import link_nodes_in_answer
from .mock_datasets import combined, desalination, flotation_leach, nickel_ew

DATASETS = [desalination.ASK, nickel_ew.ASK, flotation_leach.ASK, combined.ASK]

KEYWORDS = [
    ["осмос", "обессол", "шахтн", "вод", "desalin", "коагуля", "ионн"],
    ["электроэк", "никел", "католит", "катод", "ew", "электролит"],
    ["флотац", "выщелач", "кучн", "leach", "pax", "реагент"],
]


def pick_dataset_index(question: str) -> int:
    q = question.lower()
    for i, keys in enumerate(KEYWORDS):
        if any(k in q for k in keys):
            return i
    return len(DATASETS) - 1


def get_ask(question: str) -> dict:
    response = copy.deepcopy(DATASETS[pick_dataset_index(question)])
    answer = response["answer"]
    prefix = f"По запросу «{question}»: "

    if "answer_links" in response:
        answer_links = response["answer_links"]
        for answer_link in answer_links:
            if type(answer_link["start"]) == int:
                answer_link["start"] = answer_link["start"] + len(prefix)

            if type(answer_link["end"]) == int:
                answer_link["end"] = answer_link["end"] + len(prefix)
        response["answer_links"] = answer_links

    if not answer.startswith(prefix):
        response["answer"] = prefix + answer[0].lower() + answer[1:]
    return response


ASK = combined.ASK
GRAPH = ASK["graph"]

COMPARE = {
    "question": "электроэкстракция никеля циркуляция католита",
    "rows": [
        {"doc_id": "ni_ew_foreign", "title": "Nickel electrowinning", "year": 2022,
         "geo": "foreign", "numbers": [{"property": "скорость циркуляции католита",
                                        "op": "достигает", "value": 12, "unit": "м/с"}],
         "snippet": "optimal catholyte flow velocity of 10-12 m/s…"},
        {"doc_id": "ni_ew_ru", "title": "Электроэкстракция никеля (отеч.)", "year": 2023,
         "geo": "ru", "numbers": [{"property": "скорость циркуляции католита",
                                   "op": "в пределах", "value": ["4", "6"], "unit": "м/с"}],
         "snippet": "оптимальная скорость 4-6 м/с…"},
    ],
}

_DOCS_RAW: dict = {}
for mod in (desalination, nickel_ew, flotation_leach, combined):
    _DOCS_RAW.update(mod.DOCS)


def _mock_mentions(doc_id: str, text: str):
    nodes = []
    seen = set()
    for dataset in DATASETS:
        for node in dataset["graph"]["nodes"]:
            if doc_id in (node.get("sources") or []) and node["id"] not in seen:
                seen.add(node["id"])
                nodes.append({"id": node["id"], "label": node["label"]})
    return link_nodes_in_answer(text, nodes)


def get_document(doc_id: str):
    raw = _DOCS_RAW.get(doc_id)
    if not raw:
        raise KeyError(doc_id)
    return {**raw, "mentions": _mock_mentions(doc_id, raw["text"])}


DOC = get_document("combined_water_ni")
