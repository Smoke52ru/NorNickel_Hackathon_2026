from . import analysis
from .linking import link_nodes_in_answer

SYSTEM = ("Ты — ассистент-аналитик по горно-металлургическим данным. "
          "Отвечай только по предоставленным фрагментам. Если данных недостаточно — скажи прямо.")

ANSWER_PROMPT = """Вопрос:
{question}

Фрагменты источников:
{context}

Дай связный ответ на русском по этим фрагментам и укажи, на какие источники опираешься.
Если фрагменты не отвечают на вопрос — скажи, что в данных этого нет.
"""

EMPTY_GRAPH = {"nodes": [], "edges": []}


def _dedupe_sources(hits):
    """6 кусков одной статьи = один источник в ответе."""
    seen, out = set(), []
    for h in hits:
        if h["doc_id"] in seen:
            continue
        seen.add(h["doc_id"])
        out.append({"doc_id": h["doc_id"], "title": h.get("title", ""),
                    "year": h.get("year"), "snippet": h["text"][:200]})
    return out


def _flag_nodes(subgraph, gaps, contradictions):
    """Проставить flag узлам подграфа — фронт красит рамки, ничего не вычисляя."""
    gap_names = {g["material"].lower() for g in gaps} | {g["process"].lower() for g in gaps}
    contr_names = {c["about"].lower() for c in contradictions}
    for n in subgraph["nodes"]:
        label = n["label"].lower()
        if label in contr_names:
            n["flag"] = "contradiction"
        elif label in gap_names:
            n["flag"] = "gap"


def _filter_subgraph(subgraph, keep_node):
    nodes = [n for n in subgraph["nodes"] if keep_node(n)]
    ids = {n["id"] for n in nodes}
    edges = [e for e in subgraph["edges"] if e["from"] in ids and e["to"] in ids]
    return {"nodes": nodes, "edges": edges}


def _apply_filters(hits, subgraph, filters, graph):
    """Фильтры от фронта: годы источников, география/тип узлов, числовые диапазоны свойств."""
    if not filters:
        return hits, subgraph
    if filters.get("year_from") is not None:
        hits = [h for h in hits if (h.get("year") or 0) >= filters["year_from"]]
    if filters.get("year_to") is not None:
        hits = [h for h in hits if (h.get("year") or 9999) <= filters["year_to"]]
    if filters.get("geo"):
        subgraph = _filter_subgraph(subgraph, lambda n: n.get("geo") == filters["geo"])
    if filters.get("types"):
        allowed = set(filters["types"])
        subgraph = _filter_subgraph(subgraph, lambda n: n.get("type") in allowed)
    if filters.get("numeric") and graph:
        nf = filters["numeric"]
        docs = analysis.docs_matching_numeric(graph, nf["property"], nf.get("op", "<="), nf["value"])
        hits = [h for h in hits if h["doc_id"] in docs]
    return hits, subgraph


def answer(question, retriever, graph, llm, filters=None):
    """Полный ответ: текст + источники + подграф + пробелы/противоречия + рекомендации + цепочки."""
    hits = retriever.search(question, k=6) if retriever else []
    subgraph = graph.subgraph_for(question) if graph else dict(EMPTY_GRAPH)
    hits, subgraph = _apply_filters(hits, subgraph, filters, graph)

    if not hits:
        return {"answer": "В доступных данных не найдено информации по этому запросу.",
                "answer_links": [], "sources": [], "confidence": "low", "graph": subgraph,
                "gaps": [], "contradictions": [], "geo_gaps": [],
                "recommendations": {"experts": [], "facilities": [], "adjacent_topics": []},
                "chains": []}

    context = "\n\n".join(f"[{h['doc_id']}] {h['text'][:800]}" for h in hits)
    text = llm.generate(ANSWER_PROMPT.format(question=question, context=context), system=SYSTEM)
    sources = _dedupe_sources(hits)

    node_ids = [n["id"] for n in subgraph["nodes"]]
    names = {n["label"].lower() for n in subgraph["nodes"]}
    all_gaps = analysis.find_gaps(graph) if graph else []
    all_contr = analysis.find_contradictions(graph) if graph else []
    rel_gaps = [g for g in all_gaps if g["material"].lower() in names or g["process"].lower() in names]
    rel_contr = [c for c in all_contr if c["about"].lower() in names]

    out_gaps = (rel_gaps or all_gaps[:3])[:5]
    out_contr = (rel_contr or all_contr[:3])[:5]
    _flag_nodes(subgraph, out_gaps if rel_gaps else [], out_contr if rel_contr else [])

    return {
        "answer": text,
        "answer_links": link_nodes_in_answer(text, subgraph["nodes"]),
        "sources": sources,
        "confidence": "high" if len(sources) >= 3 else "medium",
        "graph": subgraph,
        "gaps": out_gaps,
        "contradictions": out_contr,
        "geo_gaps": [x for x in (analysis.find_geo_gaps(graph) if graph else [])
                     if x["topic"].lower() in names][:5],
        "recommendations": analysis.recommend(graph, node_ids) if graph
        else {"experts": [], "facilities": [], "adjacent_topics": []},
        "chains": analysis.causal_chains(graph, node_ids) if (graph and node_ids) else [],
    }


def _doc_geo(graph, doc_id):
    counts = {}
    for _, d in graph.g.nodes(data=True):
        if doc_id in (d.get("sources") or []):
            counts[d.get("geo", "unknown")] = counts.get(d.get("geo", "unknown"), 0) + 1
    counts.pop("unknown", None)
    return max(counts, key=counts.get) if counts else "unknown"


def _doc_numbers(graph, doc_id):
    out = []
    for n, d in graph.g.nodes(data=True):
        if d.get("type") != "Property":
            continue
        for m in d.get("measurements") or []:
            if m.get("source") == doc_id and m.get("value") is not None:
                out.append({"property": d.get("name", n), "op": m.get("op"),
                            "value": m.get("value"), "unit": m.get("unit")})
    return out


def compare(question, retriever, graph):
    """Сравнительная таблица по теме: строка = источник, колонки = год, гео, числа, вырезка."""
    hits = retriever.search(question, k=8) if retriever else []
    rows = {}
    for h in hits:
        if h["doc_id"] in rows:
            continue
        rows[h["doc_id"]] = {
            "doc_id": h["doc_id"], "title": h.get("title", ""), "year": h.get("year"),
            "geo": _doc_geo(graph, h["doc_id"]) if graph else "unknown",
            "numbers": _doc_numbers(graph, h["doc_id"]) if graph else [],
            "snippet": h["text"][:200],
        }
    return {"question": question, "rows": list(rows.values())}
