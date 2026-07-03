import json
import re

from rank_bm25 import BM25Okapi


def _tok(s):
    return re.findall(r"\w+", s.lower())


class BM25Retriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.bm25 = BM25Okapi([_tok(c["text"]) for c in chunks]) if chunks else None

    def search(self, query, k=5):
        if not self.bm25:
            return []
        scores = self.bm25.get_scores(_tok(query))
        order = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [self.chunks[i] for i in order if scores[i] > 0]

    @classmethod
    def from_jsonl(cls, path):
        chunks = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                for ch in d.get("chunks") or [d.get("text", "")]:
                    if ch:
                        chunks.append({"doc_id": d["doc_id"], "title": d.get("title", ""),
                                       "year": d.get("year"), "text": ch})
        return cls(chunks)
