import re


def _sources(node):
    return set(node.get("sources") or [])


def _words(name):
    return [w for w in re.split(r"\W+", (name or "").lower()) if len(w) >= 4]


def _same_topic(q_words, p_words):
    """Слова про одно понятие, если совпадает 5-символьный префикс (переживает окончания:
    «сульфаты» ~ «сульфатов»)."""
    return any(q[:5] == p[:5] for q in q_words for p in p_words)


def _name(g, n):
    return g.nodes[n].get("name", n)


def find_contradictions(graph):
    """Найти противоречия двумя путями:
    1) явные рёбра contradicts;
    2) расхождение числовых значений одного свойства из РАЗНЫХ источников
       (диапазон 10-12 из одной статьи — не противоречие, поэтому len(sources) > 1).
    """
    g = graph.g
    result = []

    for u, v, d in g.edges(data=True):
        if d.get("rel") == "contradicts":
            result.append({"about": _name(g, u),
                           "between": [_name(g, u), _name(g, v)],
                           "sources": [d.get("source")]})

    for n, d in g.nodes(data=True):
        measurements = [m for m in (d.get("measurements") or []) if m.get("value") is not None]
        distinct = {(str(m.get("value")), m.get("unit")) for m in measurements}
        sources = {m.get("source") for m in measurements}
        if len(distinct) > 1 and len(sources) > 1:
            result.append({"about": _name(g, n), "values": measurements,
                           "sources": sorted(sources)})

    return result


def find_gaps(graph, limit=20):
    """Неизученные комбинации материал × процесс.

    Пара «изучена», если материал и процесс делят хотя бы один источник. Пробел = пары нет,
    но оба по отдельности где-то изучались. Ранжируем по связности обоих.
    """
    g = graph.g
    materials = {n: d for n, d in g.nodes(data=True) if d.get("type") == "Material"}
    processes = {n: d for n, d in g.nodes(data=True) if d.get("type") == "Process"}

    observed = {(m, p) for m, md in materials.items() for p, pd in processes.items()
                if _sources(md) & _sources(pd)}
    mat_procs = {m: {p for (mm, p) in observed if mm == m} for m in materials}
    proc_mats = {p: {m for (m, pp) in observed if pp == p} for p in processes}

    gaps = []
    for m, md in materials.items():
        for p, pd in processes.items():
            if (m, p) in observed or not mat_procs[m] or not proc_mats[p]:
                continue
            gaps.append({"material": md.get("name", m), "process": pd.get("name", p),
                         "reason": f"{pd.get('name', p)} изучали с другими материалами "
                                   f"({len(proc_mats[p])}), а с «{md.get('name', m)}» — нет",
                         "score": len(mat_procs[m]) * len(proc_mats[p])})

    gaps.sort(key=lambda x: -x["score"])
    return gaps[:limit]


def find_geo_gaps(graph):
    """Темы, освещённые только в отечественной ИЛИ только в зарубежной практике —
    прямой пункт ТЗ про пробелы по географии."""
    g = graph.g
    out = []
    for n, d in g.nodes(data=True):
        if d.get("type") != "Process":
            continue
        geos = {d.get("geo", "unknown")}
        for x in set(g.successors(n)) | set(g.predecessors(n)):
            geos.add(g.nodes[x].get("geo", "unknown"))
        geos.discard("unknown")
        if geos == {"ru"}:
            out.append({"topic": d.get("name", n), "only": "отечественная практика"})
        elif geos == {"foreign"}:
            out.append({"topic": d.get("name", n), "only": "зарубежная практика"})
    return out


_OPS = {"<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b, "=": lambda a, b: a == b, "==": lambda a, b: a == b}


def _num(v):
    """Число из значения измерения. Диапазон ([200, 300]) сводим к среднему."""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, list) and v:
        try:
            return sum(float(x) for x in v) / len(v)
        except (TypeError, ValueError):
            return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def docs_matching_numeric(graph, prop_query, op, value):
    """doc_id, у которых есть измерение свойства (совпадение по основам слов),
    удовлетворяющее условию op value. Для запросов вида «сульфаты < 200 мг/л»."""
    qwords = _words(prop_query)
    cmp = _OPS.get(op, _OPS["<="])
    out = set()
    for n, d in graph.g.nodes(data=True):
        if d.get("type") != "Property" or not _same_topic(qwords, _words(d.get("name", ""))):
            continue
        for m in d.get("measurements") or []:
            num = _num(m.get("value"))
            if num is not None and cmp(num, value):
                out.add(m.get("source"))
    return out


def recommend(graph, node_ids):
    """Рекомендации из окружения темы: эксперты, лаборатории, смежные темы (пункт ТЗ)."""
    g = graph.g
    seeds = set(node_ids)
    ring = set(seeds)
    for _ in range(2):  # два шага по графу
        nxt = set()
        for n in ring:
            nxt |= set(g.successors(n)) | set(g.predecessors(n))
        ring |= nxt

    def pick(types, exclude_seeds=False):
        ids = [i for i in ring if g.nodes[i].get("type") in types
               and not (exclude_seeds and i in seeds)]
        ids.sort(key=lambda i: -g.degree(i))
        seen, out = set(), []
        for i in ids:
            nm = g.nodes[i].get("name", i)
            if nm not in seen:
                seen.add(nm)
                out.append(nm)
        return out

    return {"experts": pick({"Expert"})[:5],
            "facilities": pick({"Facility"})[:5],
            "adjacent_topics": pick({"Process", "Material", "Property"}, exclude_seeds=True)[:8]}


def causal_chains(graph, node_ids, limit=6):
    """Цепочки «A → B → C» внутри темы (материал→процесс→свойство и т.п.)."""
    g = graph.g.subgraph(node_ids)
    seen, chains = set(), []
    for a, b in g.edges():
        for c in g.successors(b):
            key = (a, b, c)
            if c != a and key not in seen:
                seen.add(key)
                chains.append([_name(g, a), _name(g, b), _name(g, c)])
    return chains[:limit]
