"""Mock ASK: комбинированный сквозной граф — вода, электролиз, утилизация."""

_ANSWER = (
    "На обогатительной фабрике обессоливание шахтных вод обеспечивает качество "
    "процессной воды для электроэкстракции никеля. Сульфатные растворы после "
    "выщелачивания проходят очистку и поступают в цех электролиза. "
    "Шлам после коагуляции требует утилизации; прямых данных о совместимости "
    "шламов с мембранами РО и электролитом недостаточно."
)

ASK = {
    "answer": _ANSWER,
    "answer_links": [
        {"nodeId": "обессоливание_воды", "start": 25, "end": 55,
         "label": "обессоливание шахтных вод"},
        {"nodeId": "электроэкстракция_никеля", "start": 95, "end": 119,
         "label": "электроэкстракция никеля"},
        {"nodeId": "утилизация_шлама", "start": 175, "end": 193,
         "label": "утилизация шлама"},
    ],
    "sources": [
        {"doc_id": "combined_water_ni",
         "title": "Водоподготовка для гидрометallurgии никеля",
         "year": 2023,
         "snippet": "Обессоливание шахтных вод снижает минeralизацию до 800 мг/дм³ для электролиза."},
        {"doc_id": "combined_ew_sludge",
         "title": "Электроэкстракция и стоки обогатительной фабрики",
         "year": 2022,
         "snippet": "Сульфатные растворы после выщелachivания требуют дополнительной очистки."},
        {"doc_id": "combined_sludge",
         "title": "Утилизация шламов водоподготовки",
         "year": 2021,
         "snippet": "Шлам после коagulyatsii содержит до 40% сухих веществ; утилизация — открытый вопрос."},
    ],
    "confidence": "high",
    "graph": {
        "nodes": [
            # Кластер A — водоподготовка
            {"id": "шахтные_воды", "label": "шахтные воды",
             "type": "Material", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            {"id": "обессоливание_воды", "label": "обессоливание воды",
             "type": "Process", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            {"id": "минерализация_800", "label": "минерализация 800 мг/дм³",
             "type": "Property", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            {"id": "установка_ро", "label": "установка РО",
             "type": "Equipment", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            {"id": "обогатительная_фабрика", "label": "обогatitelnaya fabrika",
             "type": "Facility", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            {"id": "опыт_вода_11", "label": "опыт ВОДА-11",
             "type": "Experiment", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            {"id": "обзор_вода_ni_2023", "label": "обзор вода-Ni 2023",
             "type": "Publication", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            {"id": "иванов_ап", "label": "Иванов А.П.",
             "type": "Expert", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            {"id": "процессная_вода", "label": "процессная вода",
             "type": "Material", "geo": "ru", "flag": None, "sources": ["combined_water_ni"]},
            # Кластер B — электроэкстракция
            {"id": "электроэкстракция_никеля", "label": "электроэкстракция никеля",
             "type": "Process", "geo": "ru", "flag": None, "sources": ["combined_ew_sludge"]},
            {"id": "сульфатный_раствор", "label": "сульфатный раствор",
             "type": "Material", "geo": "ru", "flag": None, "sources": ["combined_ew_sludge"]},
            {"id": "скорость_циркуляции", "label": "скорость циркуляции 5 м/с",
             "type": "Property", "geo": "ru", "flag": "contradiction",
             "sources": ["combined_ew_sludge", "combined_water_ni"]},
            {"id": "ванна_электроэкстракции", "label": "ванна электроэкстракции",
             "type": "Equipment", "geo": "ru", "flag": None, "sources": ["combined_ew_sludge"]},
            {"id": "цех_электролиза", "label": "цех электролиза",
             "type": "Facility", "geo": "ru", "flag": None, "sources": ["combined_ew_sludge"]},
            {"id": "опыт_ew_15", "label": "опыт EW-15",
             "type": "Experiment", "geo": "ru", "flag": None, "sources": ["combined_ew_sludge"]},
            {"id": "статья_ew_2022", "label": "статья EW 2022",
             "type": "Publication", "geo": "ru", "flag": None, "sources": ["combined_ew_sludge"]},
            {"id": "петрова_ев", "label": "Петрова Е.В.",
             "type": "Expert", "geo": "ru", "flag": None, "sources": ["combined_ew_sludge"]},
            {"id": "никель", "label": "никель",
             "type": "Material", "geo": "ru", "flag": None, "sources": ["combined_ew_sludge"]},
            # Кластер C — утилизация шлама
            {"id": "утилизация_шлама", "label": "утилизация шлама",
             "type": "Process", "geo": "ru", "flag": None, "sources": ["combined_sludge"]},
            {"id": "шлам_коагуляции", "label": "шлам коagulyatsii",
             "type": "Material", "geo": "ru", "flag": "gap", "sources": ["combined_sludge"]},
            {"id": "сухие_вещества_40", "label": "сухие вещества 40%",
             "type": "Property", "geo": "ru", "flag": None, "sources": ["combined_sludge"]},
            {"id": "фильтр_пресс", "label": "фильтр-пресс",
             "type": "Equipment", "geo": "ru", "flag": None, "sources": ["combined_sludge"]},
            {"id": "полигон_утилизации", "label": "полигон утилизации",
             "type": "Facility", "geo": "ru", "flag": None, "sources": ["combined_sludge"]},
            {"id": "опыт_шлам_03", "label": "опыт ШЛАМ-03",
             "type": "Experiment", "geo": "ru", "flag": None, "sources": ["combined_sludge"]},
            {"id": "обзор_шлам_2021", "label": "обзор шлам 2021",
             "type": "Publication", "geo": "ru", "flag": None, "sources": ["combined_sludge"]},
            {"id": "козлов_дн", "label": "Козлов Д.Н.",
             "type": "Expert", "geo": "ru", "flag": None, "sources": ["combined_sludge"]},
            {"id": "коагуляция", "label": "коагуляция",
             "type": "Process", "geo": "ru", "flag": None, "sources": ["combined_sludge"]},
        ],
        "edges": [
            # Кластер A
            {"from": "обессоливание_воды", "to": "шахтные_воды", "label": "uses_material", "flag": "normal"},
            {"from": "обессоливание_воды", "to": "минерализация_800", "label": "produces_output", "flag": "normal"},
            {"from": "обессоливание_воды", "to": "процессная_вода", "label": "produces_output", "flag": "normal"},
            {"from": "установка_ро", "to": "обессоливание_воды", "label": "part_of", "flag": "normal"},
            {"from": "обогатительная_фабрика", "to": "установка_ро", "label": "part_of", "flag": "normal"},
            {"from": "опыт_вода_11", "to": "обессоливание_воды", "label": "validated_by", "flag": "normal"},
            {"from": "обзор_вода_ni_2023", "to": "обессоливание_воды", "label": "described_in", "flag": "normal"},
            {"from": "иванов_ап", "to": "обессоливание_воды", "label": "expert_in", "flag": "normal"},
            {"from": "опыт_вода_11", "to": "обогатительная_фабрика", "label": "part_of", "flag": "normal"},
            {"from": "обзор_вода_ni_2023", "to": "иванов_ап", "label": "described_in", "flag": "normal"},
            # Кластер B
            {"from": "электроэкстракция_никеля", "to": "сульфатный_раствор",
             "label": "uses_material", "flag": "normal"},
            {"from": "электроэкстракция_никеля", "to": "никель",
             "label": "uses_material", "flag": "normal"},
            {"from": "электроэкстракция_никеля", "to": "скорость_циркуляции",
             "label": "operates_at_condition", "flag": "normal"},
            {"from": "ванна_электроэкстракции", "to": "электроэкстракция_никеля",
             "label": "part_of", "flag": "normal"},
            {"from": "цех_электролиза", "to": "ванна_электроэкстракции",
             "label": "part_of", "flag": "normal"},
            {"from": "опыт_ew_15", "to": "электроэкстракция_никеля",
             "label": "validated_by", "flag": "normal"},
            {"from": "статья_ew_2022", "to": "электроэкстракция_никеля",
             "label": "described_in", "flag": "normal"},
            {"from": "петрова_ев", "to": "электроэкстракция_никеля",
             "label": "expert_in", "flag": "normal"},
            {"from": "опыт_ew_15", "to": "цех_электролиза", "label": "part_of", "flag": "normal"},
            {"from": "статья_ew_2022", "to": "петрова_ев", "label": "described_in", "flag": "normal"},
            # Кластер C
            {"from": "утилизация_шлама", "to": "шлам_коагуляции",
             "label": "uses_material", "flag": "normal"},
            {"from": "утилизация_шлама", "to": "сухие_вещества_40",
             "label": "produces_output", "flag": "normal"},
            {"from": "коагуляция", "to": "шлам_коагуляции",
             "label": "produces_output", "flag": "gap"},
            {"from": "фильтр_пресс", "to": "утилизация_шлама",
             "label": "part_of", "flag": "normal"},
            {"from": "полигон_утилизации", "to": "фильтр_пресс",
             "label": "part_of", "flag": "normal"},
            {"from": "опыт_шлам_03", "to": "утилизация_шлама",
             "label": "validated_by", "flag": "normal"},
            {"from": "обзор_шлам_2021", "to": "утилизация_шлама",
             "label": "described_in", "flag": "normal"},
            {"from": "козлов_дн", "to": "утилизация_шлама",
             "label": "expert_in", "flag": "normal"},
            {"from": "опыт_шлам_03", "to": "полигон_утилизации", "label": "part_of", "flag": "normal"},
            {"from": "обзор_шлам_2021", "to": "козлов_дн", "label": "described_in", "flag": "normal"},
            # Мостовые рёбра
            {"from": "процессная_вода", "to": "электроэкстракция_никеля",
             "label": "uses_material", "flag": "normal"},
            {"from": "сульфатный_раствор", "to": "обессоливание_воды",
             "label": "operates_at_condition", "flag": "normal"},
            {"from": "коагуляция", "to": "обессоливание_воды",
             "label": "part_of", "flag": "normal"},
            {"from": "обзор_шлам_2021", "to": "минерализация_800",
             "label": "described_in", "flag": "normal"},
        ],
    },
    "gaps": [
        {"material": "шлам коagulyatsii", "process": "обратный осмос",
         "reason": "нет данных о совместимости шлама с мембранами РО", "score": 4},
        {"material": "процессная вода", "process": "утилизация шлама",
         "reason": "прямых данных о влиянии шламов на качество процессной воды нет", "score": 3},
    ],
    "contradictions": [
        {"about": "скорость циркуляции при электроэкстракции после водоподготовки",
         "sources": ["combined_ew_sludge", "combined_water_ni"],
         "values": [
             {"op": "достигает", "value": 5, "unit": "м/с", "source": "combined_ew_sludge"},
             {"op": "в пределах", "value": ["4", "6"], "unit": "м/с", "source": "combined_water_ni"},
         ]},
    ],
    "geo_gaps": [{"topic": "утилизация шлама", "only": "отечественная практика"}],
    "recommendations": {
        "experts": ["Иванов А.П.", "Петрова Е.В.", "Козлов Д.Н."],
        "facilities": ["обогatitelnaya fabrika", "цех электролиза", "полигон утилизации"],
        "adjacent_topics": ["флотация", "кuchное выщelachivание", "ионный обмен"],
    },
    "chains": [
        ["шахтные воды", "обessolивание воды", "процессная вода"],
        ["сульфатный раствор", "электроэкстракция никеля", "никель"],
        ["шлам коagulyatsii", "утилизация шлама", "сухие вещества 40%"],
    ],
}

DOCS = {
    "combined_water_ni": {
        "doc_id": "combined_water_ni",
        "source_path": "sample/combined_water_ni.txt",
        "title": "Водоподготовка для гидрометallurgii nikelya",
        "year": 2023, "lang": "ru",
        "text": (
            "Обessolивanie шахтных вод снижает mineralizatsiyu do 800 mg/dm³ dlya elektroliza. "
            "Ivanov A.P. otmechaet, chto kachestvo protsessnoy vody opredelyaet effektivnost "
            "elektroekstraktsii nikelya na obogatitelnoy fabrike."
        ),
    },
    "combined_ew_sludge": {
        "doc_id": "combined_ew_sludge",
        "source_path": "sample/combined_ew_sludge.txt",
        "title": "Elektroekstraktsiya i stoki obogatitelnoy fabriki",
        "year": 2022, "lang": "ru",
        "text": (
            "Sulfatnye rastvory posle vyshelachivaniya trebuyut dopolnitelnoy ochistki. "
            "Petrova E.V. pokazala, chto skorost tsirkulyatsii 5 m/s optimalna posle "
            "vodopodgotovki v tsehe elektroliza."
        ),
    },
    "combined_sludge": {
        "doc_id": "combined_sludge",
        "source_path": "sample/combined_sludge.txt",
        "title": "Utilizatsiya shlamov vodopodgotovki",
        "year": 2021, "lang": "ru",
        "text": (
            "Shlam posle koagulyatsii soderzhit do 40% sukhikh veshchestv. "
            "Kozlov D.N. otmechaet, chto utilizatsiya shlamov na poligone — "
            "otkrytyy vopros dlya obogatitelnykh fabrik."
        ),
    },
}
