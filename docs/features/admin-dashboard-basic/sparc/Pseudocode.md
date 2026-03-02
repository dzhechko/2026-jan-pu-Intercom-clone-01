# Pseudocode: Admin Dashboard (Basic)

## DashboardPage
```
function DashboardPage():
    period = state("7d")
    { metrics, loading, error } = useDashboard(period)
    if loading: render spinner
    if error: render red error banner
    render:
        period toggle [Today | 7 days | 30 days]
        MetricCard x4: consultations, leads, avg response time, escalation rate
        LineChart: daily_trend (consultations + leads)
        BarChart: top_intents (horizontal)
```

## ConversationsPage
```
function ConversationsPage():
    conversations, total, page, loading, error = state defaults
    useEffect([page]): data = await api.getConversations(page)
    render:
        header "Conversations" + total count
        table: ID (truncated), Channel, Status (badge), Intent, Created
        empty state: "No conversations yet"
        pagination: Previous/Next (20 per page)
```

## MetricCard
```
function MetricCard({ title, value, subtitle, trend }):
    trendColor = up->green, down->red, neutral->gray
    render: white card -> title (sm gray) + value (3xl bold) + subtitle (colored)
```

## useAuth
```
function useAuth():
    token = state(localStorage.getItem("token"))
    isAuthenticated = !!token
    login(email, password):
        data = await api.login(email, password)
        localStorage.setItem("token", data.access_token)
        token = data.access_token
    logout(): localStorage.removeItem("token"), token = null
    useEffect: sync token via "storage" event (cross-tab)
    return { isAuthenticated, token, login, logout, loading, error }
```

## API Client
```
function request<T>(path, options):
    attach Bearer token from localStorage
    response = fetch(API_BASE + path, options + headers)
    if 401: clear token, redirect /login, throw "Unauthorized"
    if !ok: throw error from response body
    return response.json() as T

Endpoints:
    POST /auth/login                          -> { access_token }
    GET  /dashboard/metrics?period=           -> IMetrics
    GET  /dashboard/conversations?page=&limit -> { items, total }
    GET  /dashboard/leads?page=               -> { items, total }
    GET  /dashboard/roi?period=               -> IRoiMetrics
```

## App (Root)
```
function App():
    { isAuthenticated, login, logout } = useAuth()
    if !isAuthenticated: render LoginPage
    render Layout(onLogout):
        "/" -> DashboardPage
        "/conversations" -> ConversationsPage
        "/leads" -> LeadsPage
        "/roi" -> RoiAnalyticsPage
        "*" -> redirect to "/"
```
