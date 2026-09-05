# SupportAI Frontend

React frontend for the SupportAI multi-tenant AI customer support platform.

## Stack

- React 19 + TypeScript
- Vite 8
- React Router 7
- TanStack Query 5
- MUI (Material UI) + Tailwind CSS 4
- Axios (with token refresh interceptor)

## Development

```bash
npm install
npm run dev
```

The dev server runs on `http://localhost:5173` and proxies `/api` to the FastAPI backend on `http://localhost:8000`.

## Structure

```
src/
├── api/          # axios client + API modules
├── auth/         # AuthContext + ProtectedRoute
├── layout/       # AppLayout, Sidebar, Header
├── pages/        # route-level pages
├── App.tsx       # routing
└── main.tsx      # entry (providers)
```

## Scripts

- `npm run dev` — dev server with HMR
- `npm run build` — type-check + production build
- `npm run lint` — Oxlint
- `npm run preview` — preview production build