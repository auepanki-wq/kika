# CTF Web Hub (MVP)

Лёгкий MVP с упором на инструменты для маломощного VPS.

## Что реализовано

- Backend API:
  - `POST /api/transform`
  - `POST /api/jwt/decode`, `POST /api/jwt/sign`, `POST /api/jwt/verify`
  - `POST /api/flask-unsign/decode`, `POST /api/flask-unsign/sign`, `POST /api/flask-unsign/verify`
- Frontend как **многостраничный интерфейс**:
  - отдельные страницы под URL, Base64, Hex, HTML entities, ROT13, Caesar, Unicode normalize
  - отдельные страницы под JWT и Flask-unsign
  - `index.html` с карточками по категориям
- Контейнеризация frontend + backend через единый `docker-compose.yml`

## Быстрый старт (рекомендуется)

```bash
docker compose up --build -d
```

После запуска:
- Frontend: http://127.0.0.1:8080
- Backend health: http://127.0.0.1:8000/api/health

Остановка:

```bash
docker compose down
```

## Локальный запуск без Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
python -m http.server 5173
```

Откройте http://127.0.0.1:5173.
