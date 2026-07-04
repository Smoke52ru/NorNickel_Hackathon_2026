from . import config


def get_embedder():
    """Локальная мультиязычная модель эмбеддингов (e5-small): без облака, бесплатно, на CPU."""
    return local_embedder(config.EMBED_MODEL)


def local_embedder(model_name):
    """Грузится один раз, дальше считает на CPU. Семейство e5 обучено с префиксами
    query:/passage: — без них косинусы плохо разделяют релевантное и мусор."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    use_prefix = "e5" in model_name.lower()

    def embed(texts, is_query=False):
        if use_prefix:
            p = "query: " if is_query else "passage: "
            texts = [p + t for t in texts]
        return model.encode(list(texts), normalize_embeddings=True).tolist()

    return embed
