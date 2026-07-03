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


def answer(question, retriever, graph, llm):
    hits = retriever.search(question, k=6) if retriever else []
    subgraph = graph.subgraph_for(question) if graph else EMPTY_GRAPH

    if not hits:
        return {"answer": "В доступных данных не найдено информации по этому запросу.",
                "sources": [], "confidence": "low", "graph": subgraph,
                "gaps": [], "contradictions": []}

    context = "\n\n".join(f"[{h['doc_id']}] {h['text'][:800]}" for h in hits)
    text = llm.generate(ANSWER_PROMPT.format(question=question, context=context), system=SYSTEM)

    sources = [{"doc_id": h["doc_id"], "title": h.get("title", ""), "year": h.get("year"),
                "snippet": h["text"][:200]} for h in hits]

    names = {n["label"].lower() for n in subgraph["nodes"]}
    gaps = analysis.find_gaps(graph) if graph else []
    contradictions = analysis.find_contradictions(graph) if graph else []
    rel_gaps = [g for g in gaps if g["material"].lower() in names or g["process"].lower() in names]
    rel_contr = [c for c in contradictions if c["about"].lower() in names]

    return {
        "answer": text,
        "sources": sources,
        "confidence": "high" if len(hits) >= 4 else "medium",
        "graph": subgraph,
        "gaps": (rel_gaps or gaps[:3])[:5],
        "contradictions": (rel_contr or contradictions[:3])[:5],
    }
