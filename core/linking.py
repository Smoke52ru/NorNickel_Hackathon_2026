import re


def link_nodes_in_answer(text, nodes):
    """Найти в тексте ответа упоминания узлов графа и вернуть офсеты.

    Для каждого узла ищем в тексте фразу, начинающуюся с основы первого слова названия
    (грубый стеммер под русскую морфологию). Возвращаем непересекающиеся спаны:
    длинные совпадения вытесняют короткие внутри себя (иначе «электроэкстракция никеля»
    и «электроэкстракция» дают дубли).
    """
    spans = []
    for node in nodes:
        label = (node.get("label") or "").strip()
        if not label:
            continue
        words = [w for w in re.split(r"\W+", label.lower()) if len(w) >= 4]
        if not words:
            continue
        pattern = _label_pattern(words)
        for m in pattern.finditer(text):
            spans.append({"nodeId": node["id"], "start": m.start(),
                          "end": m.end(), "label": label})

    spans.sort(key=lambda s: (s["start"], -(s["end"] - s["start"])))
    result = []
    for s in spans:
        if result and s["start"] < result[-1]["end"]:
            # вложенное короткое совпадение — пропускаем
            continue
        result.append(s)
    return result


def _label_pattern(words):
    """Регулярка «слово-по-основе (пробел слово-по-основе)*»."""
    parts = [rf"{re.escape(w[:max(4, len(w) - 2)])}\w*" for w in words]
    return re.compile(r"\b" + r"\s+".join(parts) + r"\b", re.IGNORECASE)
