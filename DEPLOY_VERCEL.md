# Деплой на Vercel (фронт + бэкенд)

Один проект Vercel: React/Vite + FastAPI через [Vercel Services](https://vercel.com/docs/services).

> **Важно:** на Vercel бэкенд работает в **MOCK-режиме** (`MOCK=1`) — готовые ответы без torch/FAISS/LLM.
> Полный RAG с графом — на VPS (см. `DEPLOY.md`).

## Быстрый деплой

### 1. Vercel CLI

```bash
npm i -g vercel
vercel login
cd /path/to/NorNickel_Hackathon_2026
vercel          # preview
vercel --prod   # production
```

### 2. Через GitHub (рекомендуется)

1. [vercel.com/new](https://vercel.com/new) → Import репозитория.
2. **Framework Preset** → **Services** (обязательно, иначе `vercel.json` с `services` не сработает).
3. Root Directory — корень репо (не `frontend/`).
4. **Production Branch** → `dev` (Settings → Environments → Production).
5. Deploy.

Автодеплой включён **только для `dev`**:

- `vercel.json` → `"git.deploymentEnabled": { "dev": true }` — push в другие ветки не деплоится.
- **Production Branch** в Vercel → `dev`.
- **Preview Deployments** отключены в настройках проекта.

## Как устроено

| Сервис   | Папка      | URL                         |
|----------|------------|-----------------------------|
| frontend | `frontend/`| `/` — SPA                   |
| backend  | корень     | `/api/*` — FastAPI (mock)   |

- `vercel_app.py` — entrypoint, монтирует `api.main` на `/api`.
- `frontend/.env.production` — `VITE_API_URL=/api`.
- `requirements-vercel.txt` — лёгкие зависимости без torch.

## Проверка после деплоя

```bash
curl https://ВАШ-ПРОЕКТ.vercel.app/api/health
curl -X POST https://ВАШ-ПРОЕКТ.vercel.app/api/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"тест"}'
```

Swagger: `https://ВАШ-ПРОЕКТ.vercel.app/api/docs`

## Переменные окружения (опционально)

| Переменная | Сервис  | Значение | Зачем |
|------------|---------|----------|-------|
| `MOCK`     | backend | `1`      | по умолчанию уже в `vercel_app.py` |
| `MOCK`     | backend | `0`      | боевой режим — **не влезет** в serverless без доработок |

## Локальная проверка конфига

```bash
pip install -r requirements-vercel.txt
MOCK=1 uvicorn vercel_app:app --reload --port 8000
# API: http://127.0.0.1:8000/api/docs

cd frontend && npm run dev
# фронт на :3000 проксирует /api → :8000
```

## Ограничения

- Размер функции ≤ 500 МБ — полный `requirements.txt` (torch) не подходит.
- Нет `data/processed/` — только mock-ответы.
- Таймаут функции — до 30 с (в `vercel.json` → `services.backend.functions`).

## Production URL

https://nor-nickel-hackathon-2026.vercel.app

Для жюри с реальным RAG: фронт на Vercel + бэкенд на VPS, `VITE_API_URL=https://ваш-vps:8000`.
