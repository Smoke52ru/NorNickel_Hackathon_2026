import os
from dotenv import load_dotenv

load_dotenv()

LLM_BACKEND = os.getenv("LLM_BACKEND", "yandex")

YC_API_KEY = os.getenv("YC_API_KEY")
YC_FOLDER = os.getenv("YC_FOLDER")
YANDEX_MODEL = os.getenv("YANDEX_MODEL", "yandexgpt-lite")

GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")

# MOCK=1 — поднять API без данных/LLM/torch: /ask отдаёт готовый ответ (для фронта)
MOCK = os.getenv("MOCK", "") not in ("", "0", "false", "False")

# Локальная модель эмбеддингов для векторного поиска
EMBED_MODEL = os.getenv("EMBED_MODEL", "intfloat/multilingual-e5-small")

DATA_RAW = os.getenv("DATA_RAW", "data/raw")
DATA_PROCESSED = os.getenv("DATA_PROCESSED", "data/processed")
