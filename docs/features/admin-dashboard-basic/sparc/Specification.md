# Specification: Admin Dashboard (Basic)

## Pages

| Route | Page Component | Description |
|-------|---------------|-------------|
| `/` | `DashboardPage` | Metrics overview with cards + charts |
| `/conversations` | `ConversationsPage` | Paginated conversation list table |
| `/leads` | `LeadsPage` | Paginated leads table with qualification badges |
| `/roi` | `RoiAnalyticsPage` | ROI analytics: savings, funnel, channel stats |
| `/login` | `LoginPage` | Email/password form (shown when unauthenticated) |

Unauthenticated users see only `LoginPage`. All other routes are wrapped in
`Layout` (sidebar + content area). Unknown routes redirect to `/`.

## Components

### Layout (`components/Layout.tsx`)
- Fixed sidebar (w-64) with nav links: Dashboard, Conversations, Leads, ROI Analytics
- Active link highlighted via `useLocation()` path matching
- Logout button in sidebar footer
- Scrollable main content area

### MetricCard (`components/MetricCard.tsx`)
- Props: `title`, `value` (string|number), optional `subtitle`, optional `trend` (up/down/neutral)
- Trend colors: green (up), red (down), gray (neutral)

## State Management

No external state library. State is managed with React hooks:

| Hook | Location | Responsibility |
|------|----------|---------------|
| `useAuth` | `hooks/useAuth.ts` | JWT token in localStorage, login/logout, storage event sync |
| `useDashboard` | `hooks/useDashboard.ts` | Fetch metrics by period, loading/error states |
| `useState`/`useEffect` | Page components | Local pagination, period selection, API calls |

## API Client (`api/client.ts`)

- Base URL: `/api/v1` (proxied by Vite in dev, Nginx in prod)
- Generic `request<T>()` wrapper: auto-attaches Bearer token, handles 401 redirect
- Endpoints: `login`, `getMetrics`, `getConversations`, `getConversation`, `getLeads`, `getRoiMetrics`

## TypeScript Interfaces (`types/index.ts`)

- `IMetrics` -- dashboard summary (consultations, leads, response time, rates, trends)
- `IConversation` -- conversation record (id, status, channel, context, timestamps)
- `IMessage` -- single message (role, agent_type, content, metadata)
- `ILead` -- lead with contact info, qualification, intent, deal value
- `IRoiMetrics` -- ROI data (savings, funnel breakdown, channel stats, trends)
- `IUser` -- authenticated user (tenant_id, role, email)

## Backend API Endpoints Consumed

| Method | Path | Response |
|--------|------|----------|
| POST | `/api/v1/auth/login` | `{ access_token }` |
| GET | `/api/v1/dashboard/metrics?period=` | `IMetrics` |
| GET | `/api/v1/dashboard/conversations?page=&limit=` | `{ items, total }` |
| GET | `/api/v1/conversations/:id` | `IConversation & { messages }` |
| GET | `/api/v1/dashboard/leads?page=` | `{ items, total }` |
| GET | `/api/v1/dashboard/roi?period=` | `IRoiMetrics` |
