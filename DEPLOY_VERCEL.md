# Деплой на Vercel (фронт + бэкенд)

Один проект Vercel: React/Vite + FastAPI через [Vercel Services](https://vercel.com/docs/services).
Конфиг — `vercel.mjs` (ветка определяет режим бэкенда).

| Ветка | Режим | Бэкенд | URL |
|-------|-------|--------|-----|
| `dev` | mock (`MOCK=1`) | готовые ответы, без LLM/данных | Production → `nor-nickel-hackathon-2026.vercel.app` |
| `master` | боевой (`MOCK=0`) | RAG + LLM + `data/vercel/` | Preview → `*-git-master-*.vercel.app` |

## Автодеплой

В `vercel.mjs`:

```js
git: { deploymentEnabled: { dev: true, master: true } }
```

- **Production Branch** в Vercel → `dev` (Settings → Environments → Production).
- **Preview Deployments** → **включить** (иначе push в `master` не задеплоится).
- Preview Deployments отключены только для посторонних веток — `feat/*` не деплоится, если не указано в `deploymentEnabled`.

## Как устроено

| Сервис | Папка | URL |
|--------|-------|-----|
| frontend | `frontend/` | `/` — SPA |
| backend | корень | `/api/*` — FastAPI |

- `vercel_app.py` — entrypoint; на `master` выставляет `MOCK=0`, `EMBEDDER=yandex`, `DATA_PROCESSED=data/vercel`.
- `frontend/.env.production` — `VITE_API_URL=/api` (одинаково для обеих веток).
- `requirements-vercel.txt` — mock-деплой (`dev`).
- `requirements-vercel-prod.txt` — боевой деплой (`master`): FAISS, numpy, без torch.

## Переменные окружения (ветка master)

Задать в Vercel Dashboard → Environment Variables → **Preview** → scope **master**:

| Переменная | Пример | Зачем |
|------------|--------|-------|
| `YC_API_KEY` | `AQVN...` | YandexGPT + эмбеддинги |
| `YC_FOLDER` | `b1g...` | folder ID |
| `LLM_BACKEND` | `yandex` | LLM-провайдер |
| `EMBEDDER` | `yandex` | уже по умолчанию в `vercel_app.py` |
| `GIGACHAT_CREDENTIALS` | (опционально) | если `LLM_BACKEND=gigachat` |

Без ключей `/ask` на `master` вернёт 502 при вызове LLM.

## Данные для master

Артефакты лежат в `data/vercel/` (не игнорируется `.vercelignore`).

При сборке, если файлов нет, `scripts/vercel-prepare-data.sh`:
- копирует `data/sample/documents.jsonl`;
- создаёт пустой `graph.pkl`.

Для полного графа и индекса — положите в `data/vercel/` локально собранные файлы и закоммитьте:

```
data/vercel/documents.jsonl
data/vercel/graph.pkl
data/vercel/vectors.npy   # опционально
```

> Полный корпус (~5 ГБ) на Vercel не поместится. Для жюри используйте сжатый/репрезентативный набор или артефакты с облачного диска.

## Проверка

```bash
# mock (dev)
curl https://nor-nickel-hackathon-2026.vercel.app/api/health

# master (подставьте URL из Vercel после push)
curl https://ВАШ-ПРОЕКТ-git-master-*.vercel.app/api/health
# ожидается: {"status":"ok","mock":false,...}
```

## Локальная проверка

```bash
# mock
MOCK=1 pip install -r requirements-vercel.txt
MOCK=1 uvicorn vercel_app:app --reload --port 8000

# master
pip install -r requirements-vercel-prod.txt
bash scripts/vercel-prepare-data.sh
VERCEL_GIT_COMMIT_REF=master MOCK=0 YC_API_KEY=... YC_FOLDER=... \
  uvicorn vercel_app:app --reload --port 8000
```

## Ограничения master на Vercel

- Лимит функции ≤ 500 МБ — локальный torch/sentence-transformers не используем.
- Эмбеддинги только через Yandex/GigaChat API.
- Таймаут до 60 с (LLM-запросы).
- Cold start: первая загрузка FAISS/графа может занять несколько секунд.

## Production URL (mock, dev)

https://nor-nickel-hackathon-2026.vercel.app
