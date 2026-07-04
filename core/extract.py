import json

from .ontology import ENTITY_TYPES, RELATION_TYPES

SYSTEM = "Ты — экстрактор знаний из научно-технических текстов по металлургии. Отвечай только валидным JSON."

PROMPT_TEMPLATE = """Извлеки из текста сущности, связи и числовые ограничения.

Типы сущностей: {entity_types}
Типы связей: {relation_types}

Верни строго JSON:
{{
  "entities": [{{"name": "...", "type": "Material", "geo": "ru|foreign|unknown"}}],
  "relations": [{{"source": "...", "relation": "uses_material", "target": "..."}}],
  "numbers": [{{"property": "сульфаты", "op": "<=", "value": 300, "unit": "мг/л"}}]
}}

Числа с единицами извлекай точно, синонимы своди к одному имени, отсутствующее — пустой список.
Названия сущностей давай ПО-РУССКИ: английские и латинские термины переводи на русский
(electrowinning → электроэкстракция, catholyte → католит), чтобы одно понятие не двоилось по языкам.

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
