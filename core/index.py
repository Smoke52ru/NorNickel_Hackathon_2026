import numpy as np


class VectorIndex:
    def __init__(self, embedder):
        self.embedder = embedder
        self._index = None
        self._chunks = []

    def build(self, chunks):
        import faiss
        self._chunks = chunks
        vecs = np.array(self.embedder([c["text"] for c in chunks]), dtype="float32")
        faiss.normalize_L2(vecs)
        self._index = faiss.IndexFlatIP(vecs.shape[1])
        self._index.add(vecs)

    def search(self, query, k=5):
        import faiss
        q = np.array(self.embedder([query]), dtype="float32")
        faiss.normalize_L2(q)
        _, idx = self._index.search(q, k)
        return [self._chunks[i] for i in idx[0] if i >= 0]
