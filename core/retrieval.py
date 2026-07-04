import json
import os
import re

from rank_bm25 import BM25Okapi


def _tok(s):
    return re.findall(r"\w+", s.lower())


# Пороги релевантности: если запрос не проходит ни по словам, ни по смыслу — честно «данных нет».
MIN_SCORE = 2.0    # BM25 (мусорный запрос даёт ~1.5, осмысленный — от 3)
VEC_MIN = 0.80     # косинус для e5-small: релевантное/кросс-язык 0.83+, мусор ~0.75
RRF_K = 60         # сглаживающая константа Reciprocal Rank Fusion


def load_chunks(path):
    """Развернуть documents.jsonl в плоский список кусков (порядок стабильный —
    совпадает с порядком векторов в vectors.npy)."""
    chunks = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            for ch in d.get("chunks") or [d.get("text", "")]:
                if ch:
                    chunks.append({"doc_id": d["doc_id"], "title": d.get("title", ""),
                                   "year": d.get("year"), "text": ch})
    return chunks


class HybridRetriever:
    """Гибридный поиск: BM25 (точные термины) + вектор (смысл, синонимы, кросс-язык),
    объединённые через RRF. Если векторов нет (не собраны / эмбеддер недоступен) —
    деградируем до чистого BM25."""

    def __init__(self, chunks, vectors=None, embedder=None):
        self.chunks = chunks
        self.bm25 = BM25Okapi([_tok(c["text"]) for c in chunks]) if chunks else None
        self.embedder = embedder
        self.index = None
        if vectors is not None and len(vectors):
            import faiss
            self.index = faiss.IndexFlatIP(vectors.shape[1])
            self.index.add(vectors)

    def search(self, query, k=6, pool=20):
        if not self.bm25:
            return []
        bm = self.bm25.get_scores(_tok(query))
        bm_order = sorted(range(len(bm)), key=lambda i: -bm[i])[:pool]
        bm_rank = {i: r for r, i in enumerate(bm_order)}

        vec_rank, sims = {}, {}
        if self.index is not None and self.embedder is not None:
            try:
                import faiss
                import numpy as np
                qv = np.asarray(self.embedder([query], is_query=True), dtype="float32")
                faiss.normalize_L2(qv)
                dist, idx = self.index.search(qv, pool)
                for r, (i, s) in enumerate(zip(idx[0].tolist(), dist[0].tolist())):
                    if i >= 0:
                        vec_rank[i] = r
                        sims[i] = s
            except Exception:
                pass  # эмбеддер недоступен — тихо остаёмся на BM25

        scored = []
        for i in set(bm_rank) | set(vec_rank):
            # гейт релевантности: кусок проходит, если релевантен хоть по одной ветке
            if bm[i] >= MIN_SCORE or sims.get(i, 0.0) >= VEC_MIN:
                rrf = ((1 / (RRF_K + bm_rank[i]) if i in bm_rank else 0)
                       + (1 / (RRF_K + vec_rank[i]) if i in vec_rank else 0))
                scored.append((rrf, i))
        scored.sort(reverse=True)
        return [self.chunks[i] for _, i in scored[:k]]

    @classmethod
    def from_processed(cls, processed_dir, embedder=None):
        """Собрать ретривер из артефактов: documents.jsonl (обязателен) + vectors.npy (опционально)."""
        docs = os.path.join(processed_dir, "documents.jsonl")
        if not os.path.exists(docs):
            return None
        chunks = load_chunks(docs)
        vectors = None
        vpath = os.path.join(processed_dir, "vectors.npy")
        if os.path.exists(vpath):
            import numpy as np
            v = np.load(vpath)
            if len(v) == len(chunks):  # защита от рассинхрона данных и векторов
                vectors = v
        return cls(chunks, vectors=vectors, embedder=embedder)
