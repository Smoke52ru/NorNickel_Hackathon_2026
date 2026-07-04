"""Mock ASK: флотация и кучное выщелачивание — 3 кластера."""

_ANSWER = (
    "Флотация медно-никелевых руд с использованием ПАВ обеспечивает извлечение никеля "
    "до 85% при оптимальной крупности помола. Кучное выщелачивание никелевых руд "
    "в холодном климате требует специальных реагентов и утепления куч. "
    "Сульфатные растворы, полученные при выщелачивании, связаны с процессами "
    "дальнейшей переработки, но прямых сравнений с флотационными схемами мало."
)

ASK = {
    "answer": _ANSWER,
    "answer_links": [
        {"nodeId": "флотация", "start": 0, "end": 8, "label": "флотация"},
        {"nodeId": "кучное_выщелачивание", "start": 95, "end": 117,
         "label": "кучное выщелачивание"},
        {"nodeId": "пав", "start": 55, "end": 58, "label": "ПАВ"},
    ],
    "sources": [
        {"doc_id": "flotation_ni_cu",
         "title": "Флотация медно-никелевых руд: отечественный опыт",
         "year": 2022,
         "snippet": "Извлечение никеля при флотации достигает 85% при K80 = 74 мкм."},
        {"doc_id": "heap_leach_cold",
         "title": "Кучное выщелачивание в условиях Крайнего Севера",
         "year": 2021,
         "snippet": "При температуре ниже −15 °C требуется утепление куч и специальные реагенты."},
        {"doc_id": "reagents_review",
         "title": "Реагенты для флотации и выщелачивания никеля",
         "year": 2020,
         "snippet": "Ксантогенаты и ПАВ показывают различную селективность по никелю и меди."},
    ],
    "confidence": "medium",
    "graph": {
        "nodes": [
            {"id": "никелевая_руда", "label": "никелевая руда", "type": "Material",
             "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "флотация", "label": "флотация", "type": "Process",
             "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "извлечение_85", "label": "извлечение 85%", "type": "Property",
             "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "флотационная_машина", "label": "флотационная машина", "type": "Equipment",
             "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "обогатительная_фабрика_нор", "label": "обогatitelnaya fabrika Norilsk",
             "type": "Facility", "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "опыт_флот_09", "label": "опыт ФЛОТ-09", "type": "Experiment",
             "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "обзор_флотация_2022", "label": "обзор флотация 2022", "type": "Publication",
             "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "волков_сн", "label": "Волков С.Н.", "type": "Expert",
             "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "k80_74", "label": "K80 = 74 мкм", "type": "Property",
             "geo": "ru", "flag": None, "sources": ["flotation_ni_cu"]},
            {"id": "кучное_выщелачивание", "label": "кuchnoe vyshelachivanie", "type": "Process",
             "geo": "ru", "flag": None, "sources": ["heap_leach_cold"]},
            {"id": "окисленная_руда", "label": "окисленная руда", "type": "Material",
             "geo": "ru", "flag": "gap", "sources": ["heap_leach_cold"]},
            {"id": "температура_минус_15", "label": "температура −15 °C", "type": "Property",
             "geo": "ru", "flag": None, "sources": ["heap_leach_cold"]},
            {"id": "оросительная_система", "label": "оросительная система", "type": "Equipment",
             "geo": "ru", "flag": None, "sources": ["heap_leach_cold"]},
            {"id": "участок_кучного_выщелачивания", "label": "uchastok kuchnogo vyshelachivaniya",
             "type": "Facility", "geo": "ru", "flag": None, "sources": ["heap_leach_cold"]},
            {"id": "опыт_hl_04", "label": "опыт HL-04", "type": "Experiment",
             "geo": "ru", "flag": None, "sources": ["heap_leach_cold"]},
            {"id": "статья_hl_2021", "label": "статья HL 2021", "type": "Publication",
             "geo": "ru", "flag": None, "sources": ["heap_leach_cold"]},
            {"id": "морозова_тк", "label": "Морозова Т.К.", "type": "Expert",
             "geo": "ru", "flag": None, "sources": ["heap_leach_cold"]},
            {"id": "холодный_климат", "label": "холодный климат", "type": "Property",
             "geo": "ru", "flag": None, "sources": ["heap_leach_cold"]},
            {"id": "пав", "label": "ПАВ", "type": "Material",
             "geo": "foreign", "flag": None, "sources": ["reagents_review"]},
            {"id": "подбор_реагентов", "label": "подбор реагентов", "type": "Process",
             "geo": "foreign", "flag": None, "sources": ["reagents_review"]},
            {"id": "селективность_ni_cu", "label": "селективность Ni/Cu", "type": "Property",
             "geo": "foreign", "flag": "contradiction",
             "sources": ["reagents_review", "flotation_ni_cu"]},
            {"id": "дозирующая_станция", "label": "дозирующая станция", "type": "Equipment",
             "geo": "foreign", "flag": None, "sources": ["reagents_review"]},
            {"id": "химлаборатория", "label": "химлаборатория", "type": "Facility",
             "geo": "foreign", "flag": None, "sources": ["reagents_review"]},
            {"id": "опыт_реаг_02", "label": "опыт РЕАГ-02", "type": "Experiment",
             "geo": "foreign", "flag": None, "sources": ["reagents_review"]},
            {"id": "обзор_реагенты_2020", "label": "обзор реагенты 2020", "type": "Publication",
             "geo": "foreign", "flag": None, "sources": ["reagents_review"]},
            {"id": "лин_хф", "label": "Линь Х.Ф.", "type": "Expert",
             "geo": "foreign", "flag": None, "sources": ["reagents_review"]},
            {"id": "ксантогенат", "label": "ксантогенат", "type": "Material",
             "geo": "foreign", "flag": None, "sources": ["reagents_review"]},
        ],
        "edges": [
            {"from": "флотация", "to": "никелевая_руда", "label": "uses_material", "flag": "normal"},
            {"from": "флотация", "to": "извлечение_85", "label": "produces_output", "flag": "normal"},
            {"from": "флотация", "to": "k80_74", "label": "operates_at_condition", "flag": "normal"},
            {"from": "флотационная_машина", "to": "флотация", "label": "part_of", "flag": "normal"},
            {"from": "обогатительная_фабрика_нор", "to": "флотационная_машина",
             "label": "part_of", "flag": "normal"},
            {"from": "опыт_флот_09", "to": "флотация", "label": "validated_by", "flag": "normal"},
            {"from": "обзор_флотация_2022", "to": "флотация", "label": "described_in", "flag": "normal"},
            {"from": "волков_сн", "to": "флотация", "label": "expert_in", "flag": "normal"},
            {"from": "опыт_флот_09", "to": "обогатительная_фабрика_нор", "label": "part_of", "flag": "normal"},
            {"from": "обзор_флотация_2022", "to": "волков_сн", "label": "described_in", "flag": "normal"},
            {"from": "кучное_выщелачивание", "to": "окисленная_руда",
             "label": "uses_material", "flag": "normal"},
            {"from": "кучное_выщелачивание", "to": "температура_минус_15",
             "label": "operates_at_condition", "flag": "normal"},
            {"from": "кучное_выщелачивание", "to": "холодный_климат",
             "label": "operates_at_condition", "flag": "normal"},
            {"from": "оросительная_система", "to": "кучное_выщелачивание",
             "label": "part_of", "flag": "normal"},
            {"from": "участок_кучного_выщелачивания", "to": "оросительная_система",
             "label": "part_of", "flag": "normal"},
            {"from": "опыт_hl_04", "to": "кучное_выщелачивание",
             "label": "validated_by", "flag": "normal"},
            {"from": "статья_hl_2021", "to": "кучное_выщелачивание",
             "label": "described_in", "flag": "normal"},
            {"from": "морозова_тк", "to": "кучное_выщелачивание",
             "label": "expert_in", "flag": "normal"},
            {"from": "опыт_hl_04", "to": "участок_кучного_выщелачивания", "label": "part_of", "flag": "normal"},
            {"from": "статья_hl_2021", "to": "морозова_тк", "label": "described_in", "flag": "normal"},
            {"from": "подбор_реагентов", "to": "пав", "label": "uses_material", "flag": "normal"},
            {"from": "подбор_реагентов", "to": "ксантогенат", "label": "uses_material", "flag": "normal"},
            {"from": "подбор_реагентов", "to": "селективность_ni_cu",
             "label": "produces_output", "flag": "normal"},
            {"from": "дозирующая_станция", "to": "подбор_реагентов",
             "label": "part_of", "flag": "normal"},
            {"from": "химлаборатория", "to": "дозирующая_станция",
             "label": "part_of", "flag": "normal"},
            {"from": "опыт_реаг_02", "to": "подбор_реагентов",
             "label": "validated_by", "flag": "normal"},
            {"from": "обзор_реагенты_2020", "to": "подбор_реагентов",
             "label": "described_in", "flag": "normal"},
            {"from": "лин_хф", "to": "подбор_реагентов", "label": "expert_in", "flag": "normal"},
            {"from": "селективность_ni_cu", "to": "извлечение_85",
             "label": "contradicts", "flag": "contradiction"},
            {"from": "опыт_реаг_02", "to": "химлаборатория", "label": "part_of", "flag": "normal"},
            {"from": "обзор_реагенты_2020", "to": "лин_хф", "label": "described_in", "flag": "normal"},
            {"from": "волков_сн", "to": "подбор_реагентов", "label": "expert_in", "flag": "normal"},
            {"from": "флотация", "to": "пав", "label": "uses_material", "flag": "normal"},
            {"from": "морозова_тк", "to": "подбор_реагентов", "label": "expert_in", "flag": "normal"},
            {"from": "обзор_реагенты_2020", "to": "селективность_ni_cu",
             "label": "described_in", "flag": "normal"},
        ],
    },
    "gaps": [
        {"material": "окисленная руда", "process": "флотация",
         "reason": "нет экспериментов для холодного климата", "score": 4},
        {"material": "никелевая руда", "process": "кuchnoe vyshelachivanie",
         "reason": "прямых сравнений флотации и выщелachivания для одной руды нет", "score": 3},
    ],
    "contradictions": [
        {"about": "селективность Ni/Cu при подборе реагентов",
         "sources": ["reagents_review", "flotation_ni_cu"],
         "values": [
             {"op": "достигает", "value": 90, "unit": "%", "source": "reagents_review"},
             {"op": "в пределах", "value": ["75", "80"], "unit": "%", "source": "flotation_ni_cu"},
         ]},
    ],
    "geo_gaps": [{"topic": "подбор реагентов", "only": "зарубежная практика"}],
    "recommendations": {
        "experts": ["Волков С.Н.", "Морозова Т.К.", "Линь Х.Ф."],
        "facilities": ["obogatitelnaya fabrika Norilsk", "uchastok kuchnogo vyshelachivaniya"],
        "adjacent_topics": ["электроэкстракция никеля", "обessolивanie vody"],
    },
    "chains": [
        ["никелевая руда", "флотация", "извлечение 85%"],
        ["окисленная руда", "кuchnoe vyshelachivanie", "температура −15 °C"],
        ["ПАВ", "подбор реагентов", "селективность Ni/Cu"],
    ],
}

DOCS = {
    "flotation_ni_cu": {
        "doc_id": "flotation_ni_cu",
        "source_path": "sample/flotation_ni_cu.txt",
        "title": "Flotatsiya medno-nikelevykh rud: otechestvennyy opyt",
        "year": 2022, "lang": "ru",
        "text": (
            "Flotatsiya medno-nikelevykh rud obespechivaet izvlechenie nikelya do 85% "
            "pri K80 = 74 mkm. Volkov S.N. otmechaet, chto selektivnost Ni/Cu "
            "sostavlyaet 75–80% pri ispolzovanii standartnykh ksantogenatov."
        ),
    },
    "heap_leach_cold": {
        "doc_id": "heap_leach_cold",
        "source_path": "sample/heap_leach_cold.txt",
        "title": "Kuchnoe vyshelachivanie v usloviyakh Kraynego Severa",
        "year": 2021, "lang": "ru",
        "text": (
            "Kuchnoe vyshelachivanie okislennykh rud v kholodnom klimatiche trebuyet "
            "utepleniya kuch. Pri temperature nizhe −15 °C effektivnost snizhaetsya. "
            "Morozova T.K. rekomenduet spetsialnye reagenty dlya uchastka "
            "kuchnogo vyshelachivaniya."
        ),
    },
    "reagents_review": {
        "doc_id": "reagents_review",
        "source_path": "sample/reagents_review.txt",
        "title": "Reagenty dlya flotatsii i vyshelachivaniya nikelya",
        "year": 2020, "lang": "ru",
        "text": (
            "Ksantogenaty i PAV pokazyvayut razlichnuyu selektivnost po nikelyu i medi. "
            "Lin Kh.F. pokazal, chto selektivnost Ni/Cu dostigaet 90% pri podbore "
            "reagentov v khimlaboratorii. Opyt REAG-02 podtverdil rezultaty."
        ),
    },
}
