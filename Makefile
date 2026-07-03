# Удобные команды. На Windows без make — просто запускай команды справа вручную.

install:       ## поставить зависимости
	python -m venv .venv && .venv/Scripts/pip install -r requirements.txt

parse:         ## распарсить документы -> documents.jsonl
	python -m ingest.parse --input data/raw --output data/processed/documents.jsonl

build:         ## собрать граф + индекс
	python scripts/build.py --input data/processed/documents.jsonl --output data/processed

api:           ## запустить бэкенд
	uvicorn api.main:app --reload

front:         ## запустить фронтенд
	cd frontend && npm install && npm run dev
