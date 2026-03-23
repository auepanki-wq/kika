# CTF Web Hub (MVP)

Лёгкий MVP с упором на декодеры/энкодеры для маломощного VPS.

## Что реализовано

- FastAPI endpoint `POST /api/transform`
- Кодеки: URL, Base64, Hex, HTML entities, ROT13, Caesar, Unicode normalize
- Простой frontend для ручного тестирования

## Запуск backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Запуск frontend

```bash
cd frontend
python -m http.server 5173
```

Откройте http://127.0.0.1:5173 и укажите API base URL.
