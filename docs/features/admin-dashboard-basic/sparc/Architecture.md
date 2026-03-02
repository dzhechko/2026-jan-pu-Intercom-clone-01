# Architecture: Admin Dashboard (Basic)

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | React | 18.3 |
| Language | TypeScript | 5.5 (strict mode) |
| Styling | Tailwind CSS | 3.4 |
| Charts | Recharts | 2.12 |
| Routing | react-router-dom | 6.26 |
| Build | Vite | 5.3 |

No external state library. Plain fetch via custom API client.

## Component Tree

```
BrowserRouter (main.tsx)
  App
    LoginPage                     [unauthenticated]
    Layout                        [authenticated]
      Sidebar (nav links, logout)
      Routes
        DashboardPage  -> MetricCard x4, LineChart, BarChart
        ConversationsPage -> Table + Pagination
        LeadsPage -> Table + Pagination
        RoiAnalyticsPage -> MetricCard x4, PieChart, BarChart, LineChart
```

## Data Flow

```
Browser -> fetch(/api/v1/*) -> Vite proxy (dev) / Nginx (prod) -> FastAPI -> PostgreSQL
```

1. `api/client.ts` reads JWT from localStorage, attaches as Bearer header.
2. On 401 response, token is cleared and user is redirected to `/login`.
3. Each page calls `api.*` in `useEffect` or custom hook.
4. Loading/error states managed locally per component.

## Authentication Flow

```
LoginPage -> POST /auth/login -> { access_token }
          -> localStorage.setItem("token") -> App re-renders -> Layout shown
Logout    -> clear localStorage -> App re-renders -> LoginPage shown
```

## Routing

| Path | Component | Auth |
|------|-----------|:----:|
| `/` | DashboardPage | Yes |
| `/conversations` | ConversationsPage | Yes |
| `/leads` | LeadsPage | Yes |
| `/roi` | RoiAnalyticsPage | Yes |
| `/login`, `*` | Redirect to `/` | -- |

Auth gating at App level: `!isAuthenticated` renders LoginPage instead of Layout.

## Build and Deploy

- **Dev:** `npm run dev` -- Vite dev server with HMR, API proxy to FastAPI
- **Build:** `npm run build` -- TypeScript compile + Vite production bundle
- **Prod:** Static files in `admin/dist/`, served by Nginx, API proxied to FastAPI
