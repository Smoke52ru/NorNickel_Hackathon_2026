"""Готовые ответы для MOCK-режима (config.MOCK=1): фронт разрабатывается без данных/LLM/torch.
Формат 1:1 совпадает с боевым — фронт потом переключается на реальный бэк без правок."""

_ANSWER = ("В зарубежной практике электроэкстракции никеля оптимальная скорость циркуляции "
           "католита составляет 10-12 м/с. В отечественной практике (Надеждинский завод) — "
           "4-6 м/с; более низкая скорость снижает дендритообразование на катодах.")

ASK = {
    "answer": _ANSWER,
    "answer_links": [
        {"nodeId": "скорость_циркуляции_католита", "start": 47, "end": 75,
         "label": "скорость циркуляции католита"},
        {"nodeId": "электроэкстракция_никеля", "start": 13, "end": 37,
         "label": "электроэкстракция никеля"},
    ],
    "sources": [
        {"doc_id": "ni_ew_foreign", "title": "Nickel electrowinning: catholyte flow",
         "year": 2022, "snippet": "optimal catholyte flow velocity of 10-12 m/s…"},
        {"doc_id": "ni_ew_ru", "title": "Электроэкстракция никеля (отеч. опыт)",
         "year": 2023, "snippet": "оптимальная скорость циркуляции католита 4-6 м/с…"},
    ],
    "confidence": "medium",
    "graph": {
        "nodes": [
            {"id": "электроэкстракция_никеля", "label": "электроэкстракция никеля",
             "type": "Process", "geo": "unknown", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "никель", "label": "никель", "type": "Material",
             "geo": "unknown", "flag": "gap", "sources": ["ni_ew_ru"]},
            {"id": "католит", "label": "католит", "type": "Material",
             "geo": "unknown", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "скорость_циркуляции_католита", "label": "скорость циркуляции католита",
             "type": "Property", "geo": "unknown", "flag": "contradiction",
             "sources": ["ni_ew_ru", "ni_ew_foreign"]},
        ],
        "edges": [
            {"from": "электроэкстракция_никеля", "to": "никель",
             "label": "uses_material", "flag": "normal"},
            {"from": "электроэкстракция_никеля", "to": "скорость_циркуляции_католита",
             "label": "operates_at_condition", "flag": "normal"},
        ],
    },
    "gaps": [{"material": "никель", "process": "флотация",
              "reason": "флотация изучалась с медью и кобальтом, а с никелем — нет", "score": 4}],
    "contradictions": [{"about": "скорость циркуляции католита",
                        "sources": ["ni_ew_ru", "ni_ew_foreign"],
                        "values": [{"op": "в пределах", "value": ["4", "6"], "unit": "м/с",
                                    "source": "ni_ew_ru"},
                                   {"op": "достигает", "value": 12, "unit": "м/с",
                                    "source": "ni_ew_foreign"}]}],
    "geo_gaps": [{"topic": "кучное выщелачивание", "only": "отечественная практика"}],
    "recommendations": {
        "experts": ["Иванов А.А."],
        "facilities": ["Надеждинский металлургический завод"],
        "adjacent_topics": ["флотация", "обессоливание воды", "сульфатные растворы"],
    },
    "chains": [["никель", "электроэкстракция никеля", "скорость циркуляции католита"]],
}

COMPARE = {
    "question": "электроэкстракция никеля циркуляция католита",
    "rows": [
        {"doc_id": "ni_ew_foreign", "title": "Nickel electrowinning", "year": 2022,
         "geo": "foreign", "numbers": [{"property": "скорость циркуляции католита",
                                        "op": "достигает", "value": 12, "unit": "м/с"}],
         "snippet": "optimal catholyte flow velocity 10-12 m/s…"},
        {"doc_id": "ni_ew_ru", "title": "Электроэкстракция никеля (отеч.)", "year": 2023,
         "geo": "ru", "numbers": [{"property": "скорость циркуляции католита",
                                   "op": "в пределах", "value": ["4", "6"], "unit": "м/с"}],
         "snippet": "оптимальная скорость 4-6 м/с…"},
    ],
}

DOC = {"doc_id": "ni_ew_ru", "title": "Электроэкстракция никеля (отеч. опыт)", "year": 2023,
       "lang": "ru", "source_path": "sample/ni_ew_ru.txt",
       "text": "На Надеждинском металлургическом заводе применяется электроэкстракция никеля…"}

GRAPH = ASK["graph"]
