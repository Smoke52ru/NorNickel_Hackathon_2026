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


def _apply_filters(hits, subgraph, filters):
    """Фильтры от фронта: география узлов, годы источников, типы узлов."""
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
    return hits, subgraph


def _filter_subgraph(subgraph, keep_node):
    nodes = [n for n in subgraph["nodes"] if keep_node(n)]
    ids = {n["id"] for n in nodes}
    edges = [e for e in subgraph["edges"] if e["from"] in ids and e["to"] in ids]
    return {"nodes": nodes, "edges": edges}


def answer(question, retriever, graph, llm, filters=None):
    """Полный ответ на вопрос: текст + источники + подграф + пробелы/противоречия + inline-ссылки.

    Текст модель пишет ТОЛЬКО по найденным фрагментам (заземление на источники).
    Граф и аналитика — параллельный слой поверх тех же данных, в LLM они не идут.
    """
    hits = retriever.search(question, k=6) if retriever else []
    subgraph = graph.subgraph_for(question) if graph else dict(EMPTY_GRAPH)
    hits, subgraph = _apply_filters(hits, subgraph, filters)

    if not hits:
        return {"answer": "В доступных данных не найдено информации по этому запросу.",
                "answer_links": [], "sources": [], "confidence": "low",
                "graph": subgraph, "gaps": [], "contradictions": []}

    context = "\n\n".join(f"[{h['doc_id']}] {h['text'][:800]}" for h in hits)
    text = llm.generate(ANSWER_PROMPT.format(question=question, context=context), system=SYSTEM)

    sources = _dedupe_sources(hits)

    names = {n["label"].lower() for n in subgraph["nodes"]}
    all_gaps = analysis.find_gaps(graph) if graph else []
    all_contr = analysis.find_contradictions(graph) if graph else []
    rel_gaps = [g for g in all_gaps if g["material"].lower() in names or g["process"].lower() in names]
    rel_contr = [c for c in all_contr if c["about"].lower() in names]

    # один и тот же срез идёт и в панели, и в подсветку графа
    out_gaps = (rel_gaps or all_gaps[:3])[:5]
    out_contr = (rel_contr or all_contr[:3])[:5]
    _flag_nodes(subgraph, out_gaps if rel_gaps else [], out_contr if rel_contr else [])

    # inline-ссылки: находим упоминания узлов графа прямо в тексте ответа —
    # фронт может подсветить эти спаны и открыть узел по клику
    answer_links = link_nodes_in_answer(text, subgraph["nodes"])

    return {
        "answer": text,
        "answer_links": answer_links,
        "sources": sources,
        "confidence": "high" if len(sources) >= 3 else "medium",
        "graph": subgraph,
        "gaps": out_gaps,
        "contradictions": out_contr,
    }
