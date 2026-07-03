from . import analysis

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
    """6 кусков одной статьи — это один источник, а не шесть: схлопываем по doc_id."""
    seen, out = set(), []
    for h in hits:
        if h["doc_id"] in seen:
            continue
        seen.add(h["doc_id"])
        out.append({"doc_id": h["doc_id"], "title": h.get("title", ""),
                    "year": h.get("year"), "snippet": h["text"][:200]})
    return out


def _flag_nodes(subgraph, gaps, contradictions):
    """Проставить flag узлам подграфа: фронт красит рамки, ничего не вычисляя сам."""
    gap_names = {g["material"].lower() for g in gaps} | {g["process"].lower() for g in gaps}
    contr_names = {c["about"].lower() for c in contradictions}
    for n in subgraph["nodes"]:
        label = n["label"].lower()
        if label in contr_names:
            n["flag"] = "contradiction"
        elif label in gap_names:
            n["flag"] = "gap"


def answer(question, retriever, graph, llm):
    """Полный ответ на вопрос: текст + источники + подграф + пробелы/противоречия.

    Текст модель пишет ТОЛЬКО по найденным фрагментам (заземление на источники).
    Граф и аналитика — параллельный слой поверх тех же данных, в LLM они не передаются.
    """
    hits = retriever.search(question, k=6) if retriever else []
    subgraph = graph.subgraph_for(question) if graph else dict(EMPTY_GRAPH)

    # Нет релевантных фрагментов — честно говорим «данных нет» (это фича из ТЗ, не ошибка)
    if not hits:
        return {"answer": "В доступных данных не найдено информации по этому запросу.",
                "sources": [], "confidence": "low", "graph": subgraph,
                "gaps": [], "contradictions": []}

    context = "\n\n".join(f"[{h['doc_id']}] {h['text'][:800]}" for h in hits)
    text = llm.generate(ANSWER_PROMPT.format(question=question, context=context), system=SYSTEM)

    sources = _dedupe_sources(hits)

    # Пробелы/противоречия фильтруем по теме вопроса (по узлам подграфа);
    # если по теме ничего нет — показываем немного общих по базе, чтобы панель не пустовала
    names = {n["label"].lower() for n in subgraph["nodes"]}
    all_gaps = analysis.find_gaps(graph) if graph else []
    all_contr = analysis.find_contradictions(graph) if graph else []
    rel_gaps = [g for g in all_gaps if g["material"].lower() in names or g["process"].lower() in names]
    rel_contr = [c for c in all_contr if c["about"].lower() in names]

    # в ответ и в подсветку идёт ОДИН и тот же срез — панель и граф не расходятся
    out_gaps = (rel_gaps or all_gaps[:3])[:5]
    out_contr = (rel_contr or all_contr[:3])[:5]
    _flag_nodes(subgraph, out_gaps if rel_gaps else [], out_contr if rel_contr else [])

    return {
        "answer": text,
        "sources": sources,
        "confidence": "high" if len(sources) >= 3 else "medium",
        "graph": subgraph,
        "gaps": out_gaps,
        "contradictions": out_contr,
    }
