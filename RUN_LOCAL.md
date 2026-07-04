# Локальный запуск

Два сценария:
- **A. Фронтендеру (Артём)** — нужен просто работающий API для вёрстки → mock-режим, 2 минуты.
- **B. Бэкенд (Родион)** — собрать граф и векторы из документов (тяжёлое, офлайн).

---

# A. Быстрый старт для фронта (mock-режим)

Тебе НЕ нужны ни данные, ни ключи LLM, ни torch. API отдаёт готовые ответы в **точном
боевом формате** — верстаешь спокойно, потом переключишься на реальный бэк без правок.

### Шаг 1. Поставить лёгкие пакеты
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic networkx rank-bm25 python-dotenv
```

### Шаг 2. Запустить в mock-режиме
```powershell
$env:MOCK = "1"
uvicorn api.main:app --reload
```
(на Linux/Mac: `MOCK=1 uvicorn api.main:app --reload`)

### Шаг 3. Проверить
Открой `http://127.0.0.1:8000/docs` — интерактивная форма.
`POST /ask` с телом `{ "question": "любой вопрос" }` вернёт полный ответ с графом,
источниками, `answer_links`, пробелами, противоречиями, рекомендациями и цепочками.

### Что дёргать с фронта
| Метод | Путь | Назначение |
|---|---|---|
| POST | /ask | `{question, filters?}` → ответ + граф + всё остальное |
| POST | /compare | `{question}` → сравнительная таблица источников |
| GET | /document/{doc_id} | полный текст документа |
| GET | /graph | обзорная карта знаний |

Формат ответов — в `prep/API_CONTRACT.md`. В mock-режиме поля заполнены реальными примерами,
так что можно верстать все состояния (флаги узлов, противоречия, ссылки в тексте).

Когда бэк будет развёрнут (Родион даст URL) — просто поменяй базовый адрес запросов.

---

# B. Полная сборка (Родион / бэкенд)

Готовит офлайн-артефакты (граф + векторы) на реальных данных.

### Шаг 1. Окружение
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Тяжёлое (torch, faiss, sentence-transformers) — первый раз несколько минут.

### Шаг 2. Ключи (.env)
```
LLM_BACKEND=gigachat            # пока Yandex не вернут ключ
GIGACHAT_CREDENTIALS=<ключ>
EMBEDDER=local
EMBED_MODEL=intfloat/multilingual-e5-small
```

### Шаг 3. Сборка (главный офлайн-шаг)
```powershell
python scripts/build.py --input data/sample/documents.jsonl --output data/processed --limit 0
```
LLM извлекает сущности/связи/числа → граф; локальная модель считает эмбеддинги.
Первый запуск качает e5-small (~470 МБ) один раз. Результат — `data/processed/`:
`graph.pkl`, `documents.jsonl`, `vectors.npy` (это и заливаем на VPS).

### Шаг 4. Запуск боевого API
```powershell
uvicorn api.main:app --reload      # → http://127.0.0.1:8000/docs
```

### На реальном корпусе
Когда Дубинин выдаст `documents.jsonl`:
```powershell
python scripts/build.py --input путь\documents.jsonl --output data/processed --limit 0
```
и перезапусти API.

### Если что-то не так
- `build.py` падает на LLM → проверь ключ в `.env`.
- мало RAM → `--limit 50`.
- векторы не собрались → поиск работает на BM25, не критично.
