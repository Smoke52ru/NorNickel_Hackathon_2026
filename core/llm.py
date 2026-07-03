from abc import ABC, abstractmethod

from . import config


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt, system=None, temperature=0.3, max_tokens=2000) -> str:
        ...


class YandexLLM(LLMClient):
    URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def __init__(self, api_key, folder_id, model="yandexgpt-lite"):
        self.api_key = api_key
        self.folder = folder_id
        self.model = model

    def generate(self, prompt, system=None, temperature=0.3, max_tokens=2000):
        import requests
        messages = []
        if system:
            messages.append({"role": "system", "text": system})
        messages.append({"role": "user", "text": prompt})
        body = {
            "modelUri": f"gpt://{self.folder}/{self.model}/latest",
            "completionOptions": {"stream": False, "temperature": temperature,
                                  "maxTokens": str(max_tokens)},
            "messages": messages,
        }
        headers = {"Authorization": f"Api-Key {self.api_key}", "x-folder-id": self.folder}
        r = requests.post(self.URL, headers=headers, json=body, timeout=60)
        r.raise_for_status()
        return r.json()["result"]["alternatives"][0]["message"]["text"]


class GigaChatLLM(LLMClient):
    def __init__(self, credentials, model="GigaChat"):
        from gigachat import GigaChat
        self._client = GigaChat(credentials=credentials, model=model,
                                scope="GIGACHAT_API_PERS", verify_ssl_certs=False)

    def generate(self, prompt, system=None, temperature=0.3, max_tokens=2000):
        from gigachat.models import Chat, Messages, MessagesRole
        msgs = []
        if system:
            msgs.append(Messages(role=MessagesRole.SYSTEM, content=system))
        msgs.append(Messages(role=MessagesRole.USER, content=prompt))
        resp = self._client.chat(Chat(messages=msgs, temperature=temperature, max_tokens=max_tokens))
        return resp.choices[0].message.content


_cached = None


def get_llm() -> LLMClient:
    global _cached
    if _cached is None:
        if config.LLM_BACKEND == "gigachat":
            _cached = GigaChatLLM(config.GIGACHAT_CREDENTIALS)
        else:
            _cached = YandexLLM(config.YC_API_KEY, config.YC_FOLDER, config.YANDEX_MODEL)
    return _cached
