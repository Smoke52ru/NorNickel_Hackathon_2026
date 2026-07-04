# Деплой на VPS (Ubuntu)

Цель: чтобы жюри открыли ссылку и всё работало, ничего не собирая у себя.
Судьи явно сказали на Q&A: «чтобы эксперты сами не собирали докер-контейнеры».

## 0. Что деплоим
- FastAPI-бэкенд (`api/main.py`) — эндпоинты `/ask`, `/document`, `/graph`, `/docs`.
- Артефакты сборки (`data/processed/`: graph.pkl, documents.jsonl, vectors.npy).
- Позже — собранный фронт Артёма (статика).

Пока фронта нет — жюри может тыкать `/docs` (Swagger даёт интерактивную форму к API).

## 1. Важное решение: где считать эмбеддинги
Сборка графа и векторов тяжёлая (LLM + модель эмбеддингов). На слабом VPS (2 ГБ) её лучше
**НЕ гонять**. Схема:
1. Собираем `data/processed/` **локально** (у себя): `python scripts/build.py ...`
2. Копируем готовые артефакты на сервер (scp).
3. Сервер только **обслуживает** запросы.

Оговорка: для векторного поиска серверу всё равно нужна модель эмбеддингов, чтобы
векторизовать сам вопрос. Это грузит torch (~0.5–1 ГБ RAM). Если на 2 ГБ будет тесно —
поиск сам деградирует до BM25 (без падения), либо берём тариф на 4 ГБ.

## 2. Первичная настройка сервера
```bash
ssh root@IP_СЕРВЕРА

apt update && apt -y upgrade
apt -y install python3 python3-venv python3-pip git ufw

# firewall: пускаем ssh и порт приложения
ufw allow OpenSSH
ufw allow 8000/tcp
ufw --force enable
```

## 3. Код и зависимости
```bash
git clone https://github.com/Smoke52ru/NorNickel_Hackathon_2026.git
cd NorNickel_Hackathon_2026
git checkout dev            # или master, где будет финал

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## 4. Ключи и данные
```bash
cp .env.example .env
nano .env        # вписать LLM_BACKEND=gigachat и GIGACHAT_CREDENTIALS (или yandex, когда вернут ключ)
```
Скопировать локально собранные артефакты (с локальной машины):
```bash
scp -r data/processed root@IP_СЕРВЕРА:~/NorNickel_Hackathon_2026/data/
```

## 5. Запуск
Проверка вручную:
```bash
. .venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000
```
Открыть в браузере: `http://IP_СЕРВЕРА:8000/docs` — работает.

Чтобы держалось после закрытия SSH — systemd-сервис `/etc/systemd/system/klubok.service`:
```ini
[Unit]
Description=Nauchny Klubok API
After=network.target

[Service]
WorkingDirectory=/root/NorNickel_Hackathon_2026
ExecStart=/root/NorNickel_Hackathon_2026/.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Service]
EnvironmentFile=/root/NorNickel_Hackathon_2026/.env

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable --now klubok
systemctl status klubok      # проверить, что active (running)
journalctl -u klubok -f      # логи
```

## 6. Фронт Артёма (когда будет)
Артём собирает статику (`npm run build` → папка `dist`), кладём её на сервер и раздаём.
Простой путь — отдавать статику тем же FastAPI:
```python
# в api/main.py
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
```
Либо nginx как реверс-прокси (статика + проксирование /api на uvicorn) — если будет время.

## 7. Домен и HTTPS (по желанию, необязательно)
Жюри устроит и `http://IP:8000`. Если хочется красиво: домен + nginx + certbot (Let's Encrypt).
На это время не тратим, если не осталось.

## 8. Когда включать
Дедлайн загрузки — вечер 4 июля, проверка/защита — 5 июля. VPS с почасовой оплатой
поднимаем **днём 4 июля**, деплоим, тестируем, ссылку кладём в решение. Держим включённым
до конца защиты 5 июля. Итого ~24–36 часов работы.
