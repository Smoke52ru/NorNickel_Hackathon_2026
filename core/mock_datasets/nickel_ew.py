"""Mock ASK: электроэкстракция никеля — 3 кластера (циркуляция, осаждение, электролит)."""

_ANSWER = (
    "В зарубежной практике электроэкстракции никеля оптимальная скорость циркуляции "
    "католита составляет 10–12 м/с. В отечественной практике (Надеждинский завод) — "
    "4–6 м/с; более низкая скорость снижает дендритообразование на катодах. "
    "Состав сульфатного электролита и режим осаждения на катоде определяют качество "
    "никелевого катода и текущую эффективность процесса."
)

ASK = {
    "answer": _ANSWER,
    "answer_links": [
        {"nodeId": "электроэкстракция_никеля", "start": 13, "end": 37,
         "label": "электроэкстракция никеля"},
        {"nodeId": "скорость_циркуляции_католита", "start": 47, "end": 75,
         "label": "скорость циркуляции католита"},
        {"nodeId": "осаждение_на_катоде", "start": 213, "end": 235,
         "label": "осаждение на катоде"},
    ],
    "sources": [
        {"doc_id": "ni_ew_foreign",
         "title": "Nickel electrowinning: catholyte circulation (foreign practice)",
         "year": 2022,
         "snippet": "optimal catholyte flow velocity of 10-12 m/s…"},
        {"doc_id": "ni_ew_ru",
         "title": "Электроэкстракция никеля: циркуляция католита (отечественный опыт)",
         "year": 2023,
         "snippet": "оптимальная скорость циркуляции католита 4-6 м/с…"},
        {"doc_id": "ni_electrolyte_review",
         "title": "Состав электролита при электроэкстракции никеля",
         "year": 2021,
         "snippet": "Сульфатный электролит с pH 3,5–4,0 обеспечивает стабильное осаждение."},
    ],
    "confidence": "medium",
    "graph": {
        "nodes": [
            # Кластер A — циркуляция католита
            {"id": "электроэкстракция_никеля", "label": "электроэкстракция никеля",
             "type": "Process", "geo": "unknown", "flag": None,
             "sources": ["ni_ew_ru", "ni_ew_foreign"]},
            {"id": "католит", "label": "католит", "type": "Material",
             "geo": "unknown", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "скорость_циркуляции_католита", "label": "скорость циркуляции католита",
             "type": "Property", "geo": "unknown", "flag": "contradiction",
             "sources": ["ni_ew_ru", "ni_ew_foreign"]},
            {"id": "диафрагменная_ячейка", "label": "диафрагменная ячейка",
             "type": "Equipment", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "цех_электролиза", "label": "цех электролиза",
             "type": "Facility", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "опыт_ni_ew_07", "label": "опыт Ni-EW-07",
             "type": "Experiment", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "обзор_электроэкстракции_ni", "label": "обзор электроэкстракции Ni",
             "type": "Publication", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "петрова_ев", "label": "Петрова Е.В.",
             "type": "Expert", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "скорость_10_12", "label": "скорость 10–12 м/с",
             "type": "Property", "geo": "foreign", "flag": None, "sources": ["ni_ew_foreign"]},
            # Кластер B — осаждение на катоде
            {"id": "осаждение_на_катоде", "label": "осаждение на катоде",
             "type": "Process", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "никелевый_катод", "label": "никелевый катод",
             "type": "Material", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "дендритообразование", "label": "дендритообразование",
             "type": "Property", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "ванна_электроэкстракции", "label": "ванна электроэкстракции",
             "type": "Equipment", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "надеждинский_завод", "label": "Надеждинский металлургический завод",
             "type": "Facility", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "опыт_катод_12", "label": "опыт КАТОД-12",
             "type": "Experiment", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "статья_катод_2022", "label": "статья катод 2022",
             "type": "Publication", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "иванов_аа", "label": "Иванов А.А.",
             "type": "Expert", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            {"id": "текущая_эффективность", "label": "текущая эффективность 95%",
             "type": "Property", "geo": "ru", "flag": None, "sources": ["ni_ew_ru"]},
            # Кластер C — электролит
            {"id": "сульфатный_электролит", "label": "сульфатный электролит",
             "type": "Material", "geo": "unknown", "flag": "gap", "sources": ["ni_electrolyte_review"]},
            {"id": "регулирование_ph", "label": "регулирование pH",
             "type": "Process", "geo": "unknown", "flag": None, "sources": ["ni_electrolyte_review"]},
            {"id": "ph_3_5_4", "label": "pH 3,5–4,0",
             "type": "Property", "geo": "unknown", "flag": None, "sources": ["ni_electrolyte_review"]},
            {"id": "реактор_нейтрализации", "label": "реактор нейтрализации",
             "type": "Equipment", "geo": "foreign", "flag": None, "sources": ["ni_electrolyte_review"]},
            {"id": "лаборатория_электролита", "label": "лаборатория электролита",
             "type": "Facility", "geo": "foreign", "flag": None, "sources": ["ni_electrolyte_review"]},
            {"id": "опыт_el_05", "label": "опыт EL-05",
             "type": "Experiment", "geo": "foreign", "flag": None, "sources": ["ni_electrolyte_review"]},
            {"id": "обзор_электролит_2021", "label": "обзор электролита 2021",
             "type": "Publication", "geo": "foreign", "flag": None, "sources": ["ni_electrolyte_review"]},
            {"id": "смирнов_иг", "label": "Смирнов И.Г.",
             "type": "Expert", "geo": "foreign", "flag": None, "sources": ["ni_electrolyte_review"]},
            {"id": "никель", "label": "никель",
             "type": "Material", "geo": "unknown", "flag": None, "sources": ["ni_ew_ru"]},
        ],
        "edges": [
            # Кластер A
            {"from": "электроэкстракция_никеля", "to": "католит", "label": "uses_material", "flag": "normal"},
            {"from": "электроэкстракция_никеля", "to": "скорость_циркуляции_католита",
             "label": "operates_at_condition", "flag": "normal"},
            {"from": "диафрагменная_ячейка", "to": "электроэкстракция_никеля",
             "label": "part_of", "flag": "normal"},
            {"from": "цех_электролиза", "to": "диафрагменная_ячейка",
             "label": "part_of", "flag": "normal"},
            {"from": "опыт_ni_ew_07", "to": "электроэкстракция_никеля",
             "label": "validated_by", "flag": "normal"},
            {"from": "обзор_электроэкстракции_ni", "to": "электроэкстракция_никеля",
             "label": "described_in", "flag": "normal"},
            {"from": "петрова_ев", "to": "электроэкстракция_никеля",
             "label": "expert_in", "flag": "normal"},
            {"from": "скорость_циркуляции_католита", "to": "скорость_10_12",
             "label": "contradicts", "flag": "contradiction"},
            {"from": "опыт_ni_ew_07", "to": "цех_электролиза", "label": "part_of", "flag": "normal"},
            {"from": "обзор_электроэкстракции_ni", "to": "петрова_ев",
             "label": "described_in", "flag": "normal"},
            # Кластер B
            {"from": "осаждение_на_катоде", "to": "никелевый_катод",
             "label": "uses_material", "flag": "normal"},
            {"from": "осаждение_на_катоде", "to": "дендритообразование",
             "label": "produces_output", "flag": "normal"},
            {"from": "осаждение_на_катоде", "to": "текущая_эффективность",
             "label": "produces_output", "flag": "normal"},
            {"from": "ванна_электроэкстракции", "to": "осаждение_на_катоде",
             "label": "part_of", "flag": "normal"},
            {"from": "надеждинский_завод", "to": "ванна_электроэкстракции",
             "label": "part_of", "flag": "normal"},
            {"from": "опыт_катод_12", "to": "осаждение_на_катоде",
             "label": "validated_by", "flag": "normal"},
            {"from": "статья_катод_2022", "to": "осаждение_на_катоде",
             "label": "described_in", "flag": "normal"},
            {"from": "иванов_аа", "to": "осаждение_на_катоде",
             "label": "expert_in", "flag": "normal"},
            {"from": "опыт_катод_12", "to": "надеждинский_завод", "label": "part_of", "flag": "normal"},
            {"from": "статья_катод_2022", "to": "иванов_аа", "label": "described_in", "flag": "normal"},
            # Кластер C
            {"from": "регулирование_ph", "to": "сульфатный_электролит",
             "label": "uses_material", "flag": "normal"},
            {"from": "регулирование_ph", "to": "ph_3_5_4",
             "label": "operates_at_condition", "flag": "normal"},
            {"from": "реактор_нейтрализации", "to": "регулирование_ph",
             "label": "part_of", "flag": "normal"},
            {"from": "лаборатория_электролита", "to": "реактор_нейтрализации",
             "label": "part_of", "flag": "normal"},
            {"from": "опыт_el_05", "to": "регулирование_ph",
             "label": "validated_by", "flag": "normal"},
            {"from": "обзор_электролит_2021", "to": "регулирование_ph",
             "label": "described_in", "flag": "normal"},
            {"from": "смирнов_иг", "to": "регулирование_ph",
             "label": "expert_in", "flag": "normal"},
            {"from": "сульфатный_электролит", "to": "никель",
             "label": "uses_material", "flag": "gap"},
            {"from": "опыт_el_05", "to": "лаборатория_электролита", "label": "part_of", "flag": "normal"},
            {"from": "обзор_электролит_2021", "to": "смирнов_иг", "label": "described_in", "flag": "normal"},
            # Мостовые рёбра
            {"from": "электроэкстракция_никеля", "to": "осаждение_на_катоде",
             "label": "produces_output", "flag": "normal"},
            {"from": "иванов_аа", "to": "электроэкстракция_никеля",
             "label": "expert_in", "flag": "normal"},
            {"from": "сульфатный_электролит", "to": "электроэкстракция_никеля",
             "label": "uses_material", "flag": "normal"},
            {"from": "обзор_электролит_2021", "to": "ph_3_5_4",
             "label": "described_in", "flag": "normal"},
        ],
    },
    "gaps": [
        {"material": "никель", "process": "флотация",
         "reason": "флотация изучалась с медью и кобальтом, а с никелем — нет", "score": 4},
        {"material": "сульфатный электролит", "process": "кучное выщелачивание",
         "reason": "нет данных о совместимости электролита с продуктами выщелачивания", "score": 3},
    ],
    "contradictions": [
        {"about": "скорость циркуляции католита",
         "sources": ["ni_ew_ru", "ni_ew_foreign"],
         "values": [
             {"op": "в пределах", "value": ["4", "6"], "unit": "м/с", "source": "ni_ew_ru"},
             {"op": "достигает", "value": 12, "unit": "м/с", "source": "ni_ew_foreign"},
         ]},
    ],
    "geo_gaps": [{"topic": "регулирование pH электролита", "only": "зарубежная практика"}],
    "recommendations": {
        "experts": ["Иванов А.А.", "Петрова Е.В.", "Смирнов И.Г."],
        "facilities": ["Надеждинский металлургический завод", "цех электролиза"],
        "adjacent_topics": ["флотация", "обессоливание воды", "сульфатные растворы"],
    },
    "chains": [
        ["католит", "электроэкстракция никеля", "скорость циркуляции католита"],
        ["никелевый катод", "осаждение на катоде", "дендритообразование"],
        ["сульфатный электролит", "регулирование pH", "pH 3,5–4,0"],
    ],
}

DOCS = {
    "ni_ew_ru": {
        "doc_id": "ni_ew_ru",
        "source_path": "sample/ni_ew_ru.txt",
        "title": "Электроэкстракция никеля: циркуляция католита (отечественный опыт)",
        "year": 2023, "lang": "ru",
        "text": (
            "На Надеждинском металлургическом заводе применяется электроэкстракция никеля "
            "из сульфатных растворов. Оптимальная скорость циркуляции католита "
            "в отечественной практике составляет 4-6 м/с. Повышение скорости снижает "
            "дендритообразование на никелевых катодах. Петрова Е.В. и Иванов А.А. "
            "отмечают связь режима осаждения на катоде с качеством катода."
        ),
    },
    "ni_ew_foreign": {
        "doc_id": "ni_ew_foreign",
        "source_path": "sample/ni_ew_foreign.txt",
        "title": "Nickel electrowinning: catholyte circulation (foreign practice)",
        "year": 2022, "lang": "ru",
        "text": (
            "В зарубежной практике электроэкстракции никеля циркуляция католита "
            "организуется с более высокой интенсивностью. Оптимальная скорость потока "
            "католита достигает 10-12 м/с. Такой режим повышает плотность тока "
            "и производительность ванн электроэкстракции никеля."
        ),
    },
    "ni_electrolyte_review": {
        "doc_id": "ni_electrolyte_review",
        "source_path": "sample/ni_electrolyte_review.txt",
        "title": "Состав электролита при электроэкстракции никеля",
        "year": 2021, "lang": "ru",
        "text": (
            "Сульфатный электролит с pH 3,5–4,0 обеспечивает стабильное осаждение никеля. "
            "Смирнов И.Г. показал, что регулирование pH в реакторе нейтрализации "
            "критично для качества электролита. Опыт EL-05 подтвердил результаты "
            "в лаборатории электролита."
        ),
    },
}
