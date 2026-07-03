from . import config


def get_embedder():
    if config.LLM_BACKEND == "gigachat":
        return gigachat_embedder(config.GIGACHAT_CREDENTIALS)
    return yandex_embedder(config.YC_API_KEY, config.YC_FOLDER)


def gigachat_embedder(credentials):
    from gigachat import GigaChat
    client = GigaChat(credentials=credentials, scope="GIGACHAT_API_PERS", verify_ssl_certs=False)

    def embed(texts):
        return [d.embedding for d in client.embeddings(list(texts)).data]

    return embed


def yandex_embedder(api_key, folder):
    import requests
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/textEmbedding"
    headers = {"Authorization": f"Api-Key {api_key}", "x-folder-id": folder}

    def embed(texts):
        out = []
        for t in texts:
            body = {"modelUri": f"emb://{folder}/text-search-doc/latest", "text": t}
            r = requests.post(url, headers=headers, json=body, timeout=60)
            r.raise_for_status()
            out.append(r.json()["embedding"])
        return out

    return embed
