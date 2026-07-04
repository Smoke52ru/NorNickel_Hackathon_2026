import json
import re

from rank_bm25 import BM25Okapi


def _tok(s):
    return re.findall(r"\w+", s.lower())


# Ниже этого скора совпадение случайное (общие слова вроде «как», «при»):
# на выборке мусорные запросы дают ~1.5, осмысленные — от 3 и выше.
MIN_SCORE = 2.0


class BM25Retriever:
    """Поиск релевантных кусков текста по ключевым словам (BM25).
    Для технических терминов (сульфаты, электроэкстракция) работает хорошо и не требует
    ни эмбеддингов, ни внешнего API. Векторный поиск — отдельно, в index.py."""

    def __init__(self, chunks):
        self.chunks = chunks
        self.bm25 = BM25Okapi([_tok(c["text"]) for c in chunks]) if chunks else None

    def search(self, query, k=5):
        """Вернуть k наиболее релевантных кусков со скором выше порога."""
        if not self.bm25:
            return []
        scores = self.bm25.get_scores(_tok(query))
        order = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [self.chunks[i] for i in order if scores[i] >= MIN_SCORE]

    @classmethod
    def from_jsonl(cls, path):
        """Построить индекс из documents.jsonl: разворачиваем документы в плоский список
        кусков, сохраняя doc_id/title/year для показа источников."""
        chunks = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                for ch in d.get("chunks") or [d.get("text", "")]:
                    if ch:
                        chunks.append({"doc_id": d["doc_id"], "title": d.get("title", ""),
                                       "year": d.get("year"), "text": ch})
        return cls(chunks)
