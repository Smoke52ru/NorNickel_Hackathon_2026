import json

from .ontology import ENTITY_TYPES, RELATION_TYPES

SYSTEM = "Ты — экстрактор знаний из научно-технических текстов по металлургии. Отвечай только валидным JSON."

PROMPT_TEMPLATE = """Извлеки из фрагмента научно-технического текста граф знаний.

Типы сущностей: {entity_types}
Типы связей: {relation_types}

ГЛАВНОЕ — СВЯЗИ, а не список терминов. Соединяй сущности:
- для каждого процесса укажи используемые материалы (uses_material) и результат/эффект (produces_output);
- привяжи свойства и числовые условия к процессу (operates_at_condition);
- где источник спорит с другим подходом — contradicts; кто эксперт в теме — expert_in.
Выделяй только КЛЮЧЕВЫЕ сущности, не дроби на мелочи — максимум ~12 сущностей на фрагмент.
Имена в relations должны ТОЧНО совпадать с именами в entities.

Верни строго JSON (пример показывает, сколько связей ждём):
{{
  "entities": [{{"name": "электроэкстракция никеля", "type": "Process", "geo": "ru"}},
               {{"name": "католит", "type": "Material", "geo": "unknown"}},
               {{"name": "скорость циркуляции католита", "type": "Property", "geo": "unknown"}}],
  "relations": [{{"source": "электроэкстракция никеля", "relation": "uses_material", "target": "католит"}},
                {{"source": "электроэкстракция никеля", "relation": "operates_at_condition", "target": "скорость циркуляции католита"}}],
  "numbers": [{{"property": "скорость циркуляции католита", "op": "=", "value": 5, "unit": "м/с"}}]
}}

Числа с единицами извлекай точно. Названия давай ПО-РУССКИ (electrowinning → электроэкстракция,
catholyte → католит), чтобы понятие не двоилось по языкам. Отсутствующее — пустой список.

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
