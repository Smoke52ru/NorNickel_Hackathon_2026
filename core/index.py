class VectorIndex:
    def __init__(self, embedder=None):
        self.embedder = embedder
        self._index = None
        self._chunks = []

    def build(self, chunks):
        raise NotImplementedError

    def search(self, query, k=5):
        raise NotImplementedError
