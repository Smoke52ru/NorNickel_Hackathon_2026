import json

from .ontology import ENTITY_TYPES, RELATION_TYPES

SYSTEM = "Ты — экстрактор знаний из научно-технических текстов по металлургии. Отвечай только валидным JSON."

PROMPT_TEMPLATE = """Ты строишь граф знаний по горно-металлургическим технологиям из фрагмента текста.

Тип сущности — СТРОГО одно из: Material, Process, Equipment, Property, Experiment, Publication, Expert, Facility.
Других типов не используй.
Типы связей: {relation_types}

ЧТО ИЗВЛЕКАТЬ (технологический уровень):
- Process: методы и процессы (ионный обмен, обратный осмос, электроэкстракция, флотация);
- Material: материалы, реагенты, продукты (шахтные воды, сульфаты, гипс, ионообменная смола);
- Equipment/Facility: аппараты, установки, заводы; Property: показатели (извлечение, сухой остаток);
- Expert — ТОЛЬКО люди-авторы; Publication — статьи/отчёты.

ЧТО НЕ ИЗВЛЕКАТЬ (это шум): химические формулы и ионы (OH-, HCO3-, Fe(OH)3, CaCO3),
отдельные элементы и молекулы, микроорганизмы, местоимения. Имена бери ДОСЛОВНО из текста.

СВЯЗИ — ГЛАВНОЕ. На каждый процесс дай связи: —uses_material→ материал,
—produces_output→ результат/эффект, —operates_at_condition→ свойство/условие.
Каждое имя в relations ТОЧНО совпадает с именем в entities. До ~10 сущностей, но связей максимум.

Верни строго JSON:
{{
  "entities": [{{"name": "ионный обмен", "type": "Process", "geo": "unknown"}},
               {{"name": "деминерализация воды", "type": "Process", "geo": "unknown"}},
               {{"name": "ионообменная смола", "type": "Material", "geo": "unknown"}}],
  "relations": [{{"source": "ионный обмен", "relation": "uses_material", "target": "ионообменная смола"}},
                {{"source": "ионный обмен", "relation": "produces_output", "target": "деминерализация воды"}}],
  "numbers": [{{"property": "извлечение", "op": "=", "value": 95, "unit": "%"}}]
}}

Названия давай ПО-РУССКИ (electrowinning → электроэкстракция). Отсутствующее — пустой список.

ТЕКСТ:
{text}
"""

# Защитный предел на длину фрагмента
MAX_CHARS = 8000


def build_prompt(text):
    return PROMPT_TEMPLATE.format(
        entity_types=", ".join(ENTITY_TYPES),
        relation_types=", ".join(RELATION_TYPES),
        text=text[:MAX_CHARS],
    )


def extract(text, llm):
    """Извлечь сущности, связи и числа из одного фрагмента текста через LLM."""
    raw = llm.generate(build_prompt(text), system=SYSTEM, temperature=0.0)
    return _parse_json(raw)


def _parse_json(raw):
    """Достать JSON из ответа модели. При невалидном JSON возвращаем пустой результат, чтобы не ронять пайплайн."""
    raw = raw.strip()
    if "```" in raw:
        raw = raw.split("```")[1].removeprefix("json").strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"entities": [], "relations": [], "numbers": [], "_error": raw[:200]}
    data.setdefault("entities", [])
    data.setdefault("relations", [])
    data.setdefault("numbers", [])
    return data
