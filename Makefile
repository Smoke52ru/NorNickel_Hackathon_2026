install:
	python -m venv .venv && .venv/Scripts/pip install -r requirements.txt

parse:
	python -m ingest.parse --input data/raw --output data/processed/documents.jsonl

build:
	python scripts/build.py --input data/processed/documents.jsonl --output data/processed

api:
	uvicorn api.main:app --reload

demo:
	python scripts/build.py --input data/sample/documents.jsonl --output data/processed
	uvicorn api.main:app --reload

front:
	cd frontend && npm ci && npm run dev
