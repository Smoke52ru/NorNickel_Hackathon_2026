from . import config


def get_embedder():
    """Вернуть функцию texts -> список векторов (мультиязычная, для гибридного поиска).
    По умолчанию локальная модель — не зависит от облака, бесплатна, работает на CPU."""
    if config.EMBEDDER == "yandex":
        return yandex_embedder(config.YC_API_KEY, config.YC_FOLDER)
    if config.EMBEDDER == "gigachat":
        return gigachat_embedder(config.GIGACHAT_CREDENTIALS)
    return local_embedder(config.EMBED_MODEL)


def local_embedder(model_name):
    """Локальная модель (sentence-transformers). Грузится один раз, дальше считает на CPU.
    Семейство e5 обучено с префиксами query:/passage: — без них косинусы плохо разделяют
    релевантное и мусор, поэтому проставляем их."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    use_prefix = "e5" in model_name.lower()

    def embed(texts, is_query=False):
        if use_prefix:
            p = "query: " if is_query else "passage: "
            texts = [p + t for t in texts]
        return model.encode(list(texts), normalize_embeddings=True).tolist()

    return embed


def gigachat_embedder(credentials):
    from gigachat import GigaChat
    client = GigaChat(credentials=credentials, scope="GIGACHAT_API_PERS", verify_ssl_certs=False)

    def embed(texts, is_query=False):
        return [d.embedding for d in client.embeddings(list(texts)).data]

    return embed


def yandex_embedder(api_key, folder):
    import time

    import requests
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/textEmbedding"
    headers = {"Authorization": f"Api-Key {api_key}", "x-folder-id": folder}

    def embed(texts, is_query=False):
        model = "text-search-query" if is_query else "text-search-doc"
        out = []
        for t in texts:
            body = {"modelUri": f"emb://{folder}/{model}/latest", "text": t[:4000]}
            for attempt in range(4):
                r = requests.post(url, headers=headers, json=body, timeout=60)
                if r.status_code in (429, 500, 503) and attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                r.raise_for_status()
                out.append(r.json()["embedding"])
                break
        return out

    return embed
