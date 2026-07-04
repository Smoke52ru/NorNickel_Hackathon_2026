"""Mock ASK: обессоливание шахтных вод — 3 кластера (РО, ионный обмен, коагуляция)."""

_ANSWER = (
    "Для обессоливания шахтных вод с содержанием сульфатов и хлоридов 200–300 мг/л "
    "и требуемым сухим остатком ≤1000 мг/дм³ применяются обратный осмос, ионный обмен "
    "и комбинированные схемы с предварительной коагуляцией. Обратный осмос эффективно "
    "снижает минерализацию, но требует предварительного удаления взвешенных частиц. "
    "Ионообменные установки показывают высокую селективность по кальцию и магнию."
)

ASK = {
    "answer": _ANSWER,
    "answer_links": [
        {"nodeId": "обратный_осмос", "start": 179, "end": 193, "label": "обратный осмос"},
        {"nodeId": "ионный_обмен", "start": 195, "end": 207, "label": "ионный обмен"},
        {"nodeId": "коагуляция", "start": 247, "end": 257, "label": "коагуляция"},
    ],
    "sources": [
        {"doc_id": "obzor_ochistka_vod",
         "title": "Методы очистки шахтных вод: обзор отечественной и зарубежной практики",
         "year": 2021,
         "snippet": "Обратный осмос применяется при сульфатах 200–400 мг/л, обеспечивая сухой остаток до 800 мг/дм³."},
        {"doc_id": "statya_desalination_2023",
         "title": "Комбинированные схемы обессоливания на обогатительных фабриках",
         "year": 2023,
         "snippet": "Схема «коагуляция → фильтрация → РО» показала КПД 92% при минерализации 1200 мг/дм³."},
        {"doc_id": "ion_exchange_review",
         "title": "Ионный обмен при обессоливании промышленных стоков",
         "year": 2020,
         "snippet": "Ионообменные колонны обеспечивают селективное удаление Ca²⁺ и Mg²⁺ из шахтных вод."},
    ],
    "confidence": "high",
    "graph": {
        "nodes": [
            # Кластер A — обратный осмос
            {"id": "шахтные_воды", "label": "шахтные воды", "type": "Material",
             "geo": "ru", "flag": None, "sources": ["obzor_ochistka_vod"]},
            {"id": "обратный_осмос", "label": "обратный осмос", "type": "Process",
             "geo": "ru", "flag": None, "sources": ["obzor_ochistka_vod", "statya_desalination_2023"]},
            {"id": "сухой_остаток", "label": "сухой остаток ≤1000 мг/дм³", "type": "Property",
             "geo": "ru", "flag": None, "sources": ["obzor_ochistka_vod"]},
            {"id": "установка_ро", "label": "установка РО", "type": "Equipment",
             "geo": "ru", "flag": None, "sources": ["obzor_ochistka_vod"]},
            {"id": "обогатительная_фабрика", "label": "обогатительная фабрика", "type": "Facility",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "опыт_обессоливания_14", "label": "опыт обессоливания №14", "type": "Experiment",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "обзор_очистки_вод_2021", "label": "обзор очистки вод 2021", "type": "Publication",
             "geo": "ru", "flag": None, "sources": ["obzor_ochistka_vod"]},
            {"id": "иванов_ап", "label": "Иванов А.П.", "type": "Expert",
             "geo": "ru", "flag": None, "sources": ["obzor_ochistka_vod"]},
            {"id": "сульфаты_200_300", "label": "сульфаты 200–300 мг/л", "type": "Property",
             "geo": "ru", "flag": None, "sources": ["obzor_ochistka_vod"]},
            # Кластер B — ионный обмен
            {"id": "ионный_обмен", "label": "ионный обмен", "type": "Process",
             "geo": "foreign", "flag": None, "sources": ["ion_exchange_review"]},
            {"id": "ионообменная_колонна", "label": "ионообменная колонна", "type": "Equipment",
             "geo": "foreign", "flag": None, "sources": ["ion_exchange_review"]},
            {"id": "кальций_магний", "label": "селективность по Ca/Mg", "type": "Property",
             "geo": "foreign", "flag": "contradiction", "sources": ["ion_exchange_review", "obzor_ochistka_vod"]},
            {"id": "минерализация_1200", "label": "минерализация 1200 мг/дм³", "type": "Property",
             "geo": "foreign", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "опыт_ио_03", "label": "опыт ИО-03", "type": "Experiment",
             "geo": "foreign", "flag": None, "sources": ["ion_exchange_review"]},
            {"id": "обзор_ионный_обмен", "label": "обзор ионного обмена 2020", "type": "Publication",
             "geo": "foreign", "flag": None, "sources": ["ion_exchange_review"]},
            {"id": "сидорова_мв", "label": "Сидорова М.В.", "type": "Expert",
             "geo": "foreign", "flag": None, "sources": ["ion_exchange_review"]},
            {"id": "станция_водоподготовки", "label": "станция водоподготовки", "type": "Facility",
             "geo": "foreign", "flag": None, "sources": ["ion_exchange_review"]},
            {"id": "катионит", "label": "катионит", "type": "Material",
             "geo": "foreign", "flag": None, "sources": ["ion_exchange_review"]},
            # Кластер C — коагуляция
            {"id": "коагуляция", "label": "коагуляция", "type": "Process",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "коагулянт", "label": "коагулянт", "type": "Material",
             "geo": "ru", "flag": "gap", "sources": ["statya_desalination_2023"]},
            {"id": "фильтр_пресс", "label": "фильтр-пресс", "type": "Equipment",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "кпд_92", "label": "КПД 92%", "type": "Property",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "опыт_коаг_07", "label": "опыт КОАГ-07", "type": "Experiment",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "статья_коагуляция_2023", "label": "статья коагуляция 2023", "type": "Publication",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "козлов_дн", "label": "Козлов Д.Н.", "type": "Expert",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "цех_водоподготовки", "label": "цех водоподготовки", "type": "Facility",
             "geo": "ru", "flag": None, "sources": ["statya_desalination_2023"]},
            {"id": "взвешенные_частицы", "label": "взвешенные частицы", "type": "Property",
             "geo": "ru", "flag": None, "sources": ["obzor_ochistka_vod"]},
        ],
        "edges": [
            # Кластер A — плотная связность
            {"from": "обратный_осмос", "to": "шахтные_воды", "label": "uses_material", "flag": "normal"},
            {"from": "обратный_осмос", "to": "сухой_остаток", "label": "produces_output", "flag": "normal"},
            {"from": "обратный_осмос", "to": "сульфаты_200_300", "label": "operates_at_condition", "flag": "normal"},
            {"from": "установка_ро", "to": "обратный_осмос", "label": "part_of", "flag": "normal"},
            {"from": "обогатительная_фабрика", "to": "установка_ро", "label": "part_of", "flag": "normal"},
            {"from": "опыт_обессоливания_14", "to": "обратный_осмос", "label": "validated_by", "flag": "normal"},
            {"from": "обзор_очистки_вод_2021", "to": "обратный_осмос", "label": "described_in", "flag": "normal"},
            {"from": "иванов_ап", "to": "обратный_осмос", "label": "expert_in", "flag": "normal"},
            {"from": "шахтные_воды", "to": "сульфаты_200_300", "label": "operates_at_condition", "flag": "normal"},
            {"from": "опыт_обессоливания_14", "to": "обогатительная_фабрика", "label": "part_of", "flag": "normal"},
            {"from": "обзор_очистки_вод_2021", "to": "иванов_ап", "label": "described_in", "flag": "normal"},
            # Кластер B — плотная связность
            {"from": "ионный_обмен", "to": "катионит", "label": "uses_material", "flag": "normal"},
            {"from": "ионный_обмен", "to": "кальций_магний", "label": "produces_output", "flag": "normal"},
            {"from": "ионообменная_колонна", "to": "ионный_обмен", "label": "part_of", "flag": "normal"},
            {"from": "станция_водоподготовки", "to": "ионообменная_колонна", "label": "part_of", "flag": "normal"},
            {"from": "опыт_ио_03", "to": "ионный_обмен", "label": "validated_by", "flag": "normal"},
            {"from": "обзор_ионный_обмен", "to": "ионный_обмен", "label": "described_in", "flag": "normal"},
            {"from": "сидорова_мв", "to": "ионный_обмен", "label": "expert_in", "flag": "normal"},
            {"from": "ионный_обмен", "to": "минерализация_1200", "label": "operates_at_condition", "flag": "normal"},
            {"from": "опыт_ио_03", "to": "станция_водоподготовки", "label": "part_of", "flag": "normal"},
            {"from": "обзор_ионный_обмен", "to": "сидорова_мв", "label": "described_in", "flag": "normal"},
            {"from": "кальций_магний", "to": "минерализация_1200", "label": "contradicts", "flag": "contradiction"},
            # Кластер C — плотная связность
            {"from": "коагуляция", "to": "коагулянт", "label": "uses_material", "flag": "normal"},
            {"from": "коагуляция", "to": "кпд_92", "label": "produces_output", "flag": "normal"},
            {"from": "коагуляция", "to": "взвешенные_частицы", "label": "operates_at_condition", "flag": "normal"},
            {"from": "фильтр_пресс", "to": "коагуляция", "label": "part_of", "flag": "normal"},
            {"from": "цех_водоподготовки", "to": "фильтр_пресс", "label": "part_of", "flag": "normal"},
            {"from": "опыт_коаг_07", "to": "коагуляция", "label": "validated_by", "flag": "normal"},
            {"from": "статья_коагуляция_2023", "to": "коагуляция", "label": "described_in", "flag": "normal"},
            {"from": "козлов_дн", "to": "коагуляция", "label": "expert_in", "flag": "normal"},
            {"from": "опыт_коаг_07", "to": "цех_водоподготовки", "label": "part_of", "flag": "normal"},
            {"from": "статья_коагуляция_2023", "to": "козлов_дн", "label": "described_in", "flag": "normal"},
            {"from": "коагулянт", "to": "взвешенные_частицы", "label": "operates_at_condition", "flag": "gap"},
            # Мостовые рёбра (слабая межкластерная связь)
            {"from": "иванов_ап", "to": "ионный_обмен", "label": "expert_in", "flag": "normal"},
            {"from": "обзор_ионный_обмен", "to": "минерализация_1200", "label": "described_in", "flag": "normal"},
            {"from": "коагуляция", "to": "обратный_осмос", "label": "operates_at_condition", "flag": "normal"},
            {"from": "статья_коагуляция_2023", "to": "кальций_магний", "label": "described_in", "flag": "normal"},
        ],
    },
    "gaps": [
        {"material": "коагулянт", "process": "обратный осмос",
         "reason": "нет данных о совместимости коагулянта с мембранами РО при −20 °C", "score": 4},
        {"material": "шахтные воды", "process": "ионный обмен + коагуляция",
         "reason": "отсутствуют данные при температуре ниже −20 °C", "score": 3},
    ],
    "contradictions": [
        {"about": "селективность ионного обмена по Ca/Mg",
         "sources": ["ion_exchange_review", "obzor_ochistka_vod"],
         "values": [
             {"op": "достигает", "value": 95, "unit": "%", "source": "ion_exchange_review"},
             {"op": "в пределах", "value": ["80", "85"], "unit": "%", "source": "obzor_ochistka_vod"},
         ]},
    ],
    "geo_gaps": [{"topic": "ионный обмен", "only": "зарубежная практика"}],
    "recommendations": {
        "experts": ["Иванов А.П.", "Сидорова М.В."],
        "facilities": ["обогатительная фабрика", "станция водоподготовки"],
        "adjacent_topics": ["электроэкстракция никеля", "флотация", "кучное выщелачивание"],
    },
    "chains": [
        ["шахтные воды", "обратный осмос", "сухой остаток ≤1000 мг/дм³"],
        ["катионит", "ионный обмен", "селективность по Ca/Mg"],
        ["коагулянт", "коагуляция", "КПД 92%"],
    ],
}

DOCS = {
    "obzor_ochistka_vod": {
        "doc_id": "obzor_ochistka_vod",
        "source_path": "sample/obzor_ochistka_vod.txt",
        "title": "Методы очистки шахтных вод: обзор отечественной и зарубежной практики",
        "year": 2021, "lang": "ru",
        "text": (
            "Обратный осмос применяется при сульфатах 200–400 мг/л, обеспечивая сухой остаток "
            "до 800 мг/дм³ при правильной предварительной подготовке. Иванов А.П. отмечает, "
            "что ионный обмен эффективен для селективного удаления кальция и магния из шахтных "
            "вод с минерализацией до 1500 мг/дм³. Селективность по Ca/Mg составляет 80–85%."
        ),
    },
    "statya_desalination_2023": {
        "doc_id": "statya_desalination_2023",
        "source_path": "sample/statya_desalination_2023.txt",
        "title": "Комбинированные схемы обессolивания на обогатительных фабриках",
        "year": 2023, "lang": "ru",
        "text": (
            "Схема «коагуляция → фильтрация → РО» показала КПД 92% при исходной минерализации "
            "1200 мг/дм³. Предварительная коагуляция снижает нагрузку на мембраны обратного осмоса "
            "и продлевает межпромывочный интервал. Козлов Д.Н. рекомендует коагулянт на основе "
            "гидрооксида алюминия."
        ),
    },
    "ion_exchange_review": {
        "doc_id": "ion_exchange_review",
        "source_path": "sample/ion_exchange_review.txt",
        "title": "Ионный обмен при обессоливании промышленных стоков",
        "year": 2020, "lang": "ru",
        "text": (
            "Ионообменные колонны обеспечивают селективное удаление Ca²⁺ и Mg²⁺ из шахтных вод. "
            "Сидорова М.В. показала, что селективность по Ca/Mg достигает 95% при использовании "
            "катионита. Опыт ИО-03 подтвердил эффективность на станции водоподготовки."
        ),
    },
}
