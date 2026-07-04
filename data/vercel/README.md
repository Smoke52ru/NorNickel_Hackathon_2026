# Артефакты для Vercel-деплоя (ветка master)

Файлы попадают в serverless-функцию и используются при `MOCK=0`.

| Файл | Обязателен | Описание |
|------|------------|----------|
| `documents.jsonl` | да | корпус для BM25/векторного поиска |
| `graph.pkl` | желательно | граф знаний для `/graph`, подграфов в `/ask` |
| `vectors.npy` | нет | FAISS-индекс; без него — только BM25 |

Пересборка локально:

```bash
python scripts/build.py --input data/processed/documents.jsonl --output data/vercel
# или для демо-набора:
python scripts/build.py --input data/sample/documents.jsonl --output data/vercel
```

При деплое `scripts/vercel-prepare-data.sh` заполняет минимальный набор, если файлов нет.
