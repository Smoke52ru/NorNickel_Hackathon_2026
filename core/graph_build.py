import re

from .graph_store import NetworkxGraphStore

_STOP = {"для", "при", "в", "на", "и", "с", "по", "из", "к", "от", "до"}


def _norm(name):
    """Нормализуем имя для сравнения: нижний регистр, схлопнутые пробелы."""
    return re.sub(r"\s+", " ", name.strip().lower())


def _nid(name):
    """Стабильный id узла из имени - чтобы одна и та же сущность из разных документов
    попадала в ОДИН узел (дедупликация)."""
    return re.sub(r"\W+", "_", _norm(name)).strip("_")[:60]


def _stems(name):
    """Основы слов названия (обрезаем окончания) - грубая замена стеммера"""
    words = [w for w in re.split(r"\W+", _norm(name)) if w and w not in _STOP]
    return [w[:max(4, len(w) - 2)] for w in words]


def _find_property(g, name):
    """Ищем существующий узел-свойство про ту же физическую величину.

    Считаем свойства одинаковыми, если совпадает первое слово 
    (сама величина: скорость, концентрация) и множества основ
    пересекаются хотя бы наполовину.
    """
    stems = _stems(name)
    if not stems:
        return None
    sset = set(stems)
    for n, d in g.nodes(data=True):
        if d.get("type") != "Property":
            continue
        other = _stems(d.get("name", ""))
        if not other or other[0] != stems[0]:
            continue
        if len(sset & set(other)) / len(sset | set(other)) >= 0.5:
            return n
    return None


def _add_source(node, doc_id):
    srcs = node.setdefault("sources", [])
    if doc_id not in srcs:
        srcs.append(doc_id)


def add_extraction(graph, extraction, doc_id, meta=None):
    """Влить результат извлечения одного фрагмента в граф."""
    g = graph.g

    for e in extraction.get("entities", []):
        name = e.get("name")
        if not name:
            continue
        etype = e.get("type", "Unknown")
        eid = (_find_property(g, name) if etype == "Property" else None) or _nid(name)
        if eid in g:
            _add_source(g.nodes[eid], doc_id)
        else:
            graph.add_entity(eid, etype, name,
                             geo=e.get("geo", "unknown"), sources=[doc_id])

    for r in extraction.get("relations", []):
        s, t = r.get("source"), r.get("target")
        if not s or not t:
            continue
        sid, tid = _nid(s), _nid(t)
        # Если модель упомянула в связи сущность, которую не положила в entities,
        # создаём узел-заглушку Unknown
        for nid, nm in ((sid, s), (tid, t)):
            if nid not in g:
                graph.add_entity(nid, "Unknown", nm, sources=[doc_id])
        graph.add_relation(sid, tid, r.get("relation", "related"), source=doc_id)

    for num in extraction.get("numbers", []):
        prop = num.get("property")
        if not prop:
            continue
        pid = _find_property(g, prop) or _nid(prop)
        if pid not in g:
            graph.add_entity(pid, "Property", prop, measurements=[], sources=[doc_id])
        else:
            _add_source(g.nodes[pid], doc_id)
        # Числа копим списком "измерений" на узле-свойстве - расхождения между
        # источниками потом ловит find_contradictions.
        g.nodes[pid].setdefault("measurements", []).append(
            {"op": num.get("op"), "value": num.get("value"),
             "unit": num.get("unit"), "source": doc_id})


def build_graph(documents, extractor, llm):
    """Собрать граф из списка документов (каждый прогоняется через extractor по чанкам)."""
    graph = NetworkxGraphStore()
    for doc in documents:
        for chunk in doc.get("chunks") or [doc["text"]]:
            add_extraction(graph, extractor(chunk, llm), doc["doc_id"], doc)
    return graph
