# Run Commands

## Backend (FastAPI)

Prereqs: `backend/.env` must exist with `DATABASE_URL`, `JWT_SECRET`, `SUPABASE_URL` (see `backend/.env.example`).

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

- Runs on http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### Backend tests / lint

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m ruff check app tests
```

## Frontend (React)

```powershell
cd frontend
npm run dev
```

- Runs on http://localhost:5173 (dev server with `/api` proxy to the backend on port 8000)