# API-контракт «Научный клубок» (утверждён)

Единый источник правды для фронта (Артём) и бэка. Data-слой (Дубинин) — внизу.

## POST /ask
Запрос:
```json
{ "question": "строка вопроса пользователя",
  "filters": {                        // всё опционально
    "geo": "ru|foreign",
    "year_from": 2020, "year_to": 2025,
    "types": ["Material", "Process"],
    "numeric": { "property": "сульфаты", "op": "<", "value": 200 },
    "materialKeyword": "никель",
    "processKeyword": "электроэкстракция"
  } }
```

Ответ (HTTP 200 в штатных случаях, всегда одна и та же структура):
```json
{
  "answer": "связный текст ответа",
  "sources": [
    { "doc_id": "ni_ew_ru", "title": "…", "year": 2023, "snippet": "первые ~200 симв." }
  ],
  "confidence": "high | medium | low",
  "graph": {
    "nodes": [
      { "id": "n1", "label": "Никель", "type": "Material", "flag": null }
    ],
    "edges": [
      { "from": "n2", "to": "n1", "label": "uses_material", "flag": "normal" }
    ]
  },
  "gaps": [
    { "material": "Медь", "process": "электроэкстракция", "reason": "…" }
  ],
  "contradictions": [
    { "about": "скорость циркуляции католита", "sources": ["docA","docB"], "values": [] }
  ]
}
```

Поля:
- `answer` — текст ответа. Всегда строка (может быть «данных нет»).
- `sources` — источники ответа. `doc_id` — ключ для перехода к документу.
- `confidence` — уверенность: high/medium/low.
- `graph.nodes` — кружки. `type` ∈ {Material, Process, Equipment, Property, Experiment, Publication, Expert, Facility, Unknown} → цвет. `flag` (null | "contradiction" | "gap") → подсветка узла.
- `graph.edges` — линии. `from`/`to` = id узлов. `label` = тип связи. `flag` (normal | contradiction | gap) → цвет/стиль линии.
- `gaps`, `contradictions` — списки для боковой панели (текстом). Могут быть пустыми.

Любой список может быть пустым — фронт это учитывает.

## GET /document/{doc_id}
Полный текст документа + позиции упоминаний сущностей графа в этом тексте.
`mentions[]` — где в `text` встречаются сущности (по `nodeId` фронт находит нужную и
подсвечивает/скроллит к ней). start/end — индексы символов в `text`.
```json
{ "doc_id": "ni_ew_ru", "title": "…", "year": 2023, "source_path": "…",
  "text": "полный текст",
  "mentions": [ { "nodeId": "электроэкстракция_никеля", "start": 52, "end": 76,
                  "label": "электроэкстракция никеля" } ] }
```

## Ошибки
- Нет поля `question` / некорректный запрос → 422 (FastAPI сам). Фронт: «введите вопрос».
- Внутренняя ошибка → 500. Фронт: проверять `response.ok`, показывать «ошибка сервера».
- «Нет ответа в данных» — это НЕ ошибка: HTTP 200, `answer` = честное «в данных не найдено», `confidence: low`, пустые `sources`/`graph`. Фронт рисует состояние «🔍 Данных нет».

## documents.jsonl (data-слой, Дубинин → бэк; фронт напрямую не читает)
```json
{ "doc_id", "source_path", "title", "year", "lang", "text", "chunks": ["…"] }
```
`doc_id` — сквозной ключ: документ → источники/узлы в ответе /ask → GET /document.

## Маппинг в vis-network
Наш JSON почти 1:1 ложится на vis-network:
- `graph.nodes` → DataSet nodes: `id`, `label`, `group = type` (цвет группы), опц. рамка по `flag`.
- `graph.edges` → DataSet edges: `from`, `to`, `label`, цвет/`dashes` по `flag`.
