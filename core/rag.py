SYSTEM = ("Ты — ассистент-аналитик по горно-металлургическим данным. "
          "Отвечай только по предоставленным фрагментам. Если данных недостаточно — скажи прямо.")

ANSWER_PROMPT = """Вопрос:
{question}

Фрагменты источников:
{context}

Дай связный ответ на русском по этим фрагментам и укажи, на какие источники опираешься.
Если фрагменты не отвечают на вопрос — скажи, что в данных этого нет.
"""


def answer(question, index, graph, llm):
    hits = index.search(question, k=6) if index else []
    if not hits:
        return {
            "answer": "В доступных данных не найдено информации по этому запросу.",
            "sources": [], "confidence": "low",
            "graph": {"nodes": [], "edges": []}, "gaps": [], "contradictions": [],
        }

    context = "\n\n".join(f"[{h['doc_id']}] {h['text']}" for h in hits)
    text = llm.generate(ANSWER_PROMPT.format(question=question, context=context), system=SYSTEM)

    sources = [{"doc_id": h["doc_id"], "title": h.get("title", ""), "year": h.get("year"),
                "snippet": h["text"][:200]} for h in hits]

    return {
        "answer": text,
        "sources": sources,
        "confidence": "high" if len(hits) >= 4 else "medium",
        "graph": {"nodes": [], "edges": []},
        "gaps": [],
        "contradictions": [],
    }
