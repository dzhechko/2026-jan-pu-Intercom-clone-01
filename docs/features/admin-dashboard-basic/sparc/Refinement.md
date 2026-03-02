# Refinement: Admin Dashboard (Basic)

## Edge Cases

### EC-1: Auth Token Expired
**Trigger:** JWT expires (1h TTL) while user is on the dashboard.
**Handling:** `api/client.ts` checks 401, clears localStorage, redirects to `/login`.
**Risk:** Mid-session redirect with no warning. No refresh token mechanism yet.
**Improvement:** Add refresh tokens (7d TTL) with silent renewal.

### EC-2: API Unreachable / Server Error
**Trigger:** Backend container down, network timeout, or 500 response.
**Handling:** Each page catches fetch errors, renders red error banner with message.
**Risk:** Generic "Failed to fetch" message is unhelpful.
**Improvement:** Add retry button. Distinguish network vs server errors.

### EC-3: Empty Metrics (No Data)
**Trigger:** Fresh deployment, no conversations or leads exist.
**Handling:** Cards show 0/"N/A", tables show "No X yet" rows, charts render empty.
**Risk:** Charts with zero data render empty axes.
**Improvement:** Show onboarding prompt when no data exists.

### EC-4: Responsive Layout
**Trigger:** User on tablet or mobile browser.
**Handling:** Tailwind responsive classes on grids, `ResponsiveContainer` on charts.
**Risk:** Sidebar (w-64) does not collapse on small screens.
**Improvement:** Add hamburger toggle for sidebar on screens < 768px.

### EC-5: Long Conversation / Lead Lists
**Trigger:** Thousands of conversations in production.
**Handling:** Server-side pagination (20/page), Previous/Next buttons.
**Risk:** No search, filter, or column sorting.
**Improvement:** Add search, status/channel filters, sortable headers.

### EC-6: Concurrent Tab Sessions
**Trigger:** User logs out in one tab while another tab is open.
**Handling:** `useAuth` listens for `storage` events; 401 handler also clears token.
**Risk:** In-flight requests may 401 before storage event propagates.
**Mitigation:** Both paths (storage + 401) converge to login page independently.

### EC-7: XSS via Conversation Content
**Trigger:** Malicious content in messages or lead contact fields.
**Handling:** React auto-escapes JSX. No `dangerouslySetInnerHTML` used.
**Risk:** Low. CSP header in Nginx config adds defense-in-depth.

## Testing Priorities

| Priority | Area | Test Type |
|----------|------|-----------|
| High | Auth flow (login, 401 redirect, logout) | Integration |
| High | Dashboard metric rendering with mock data | Unit |
| Medium | Pagination (page boundaries, empty state) | Unit |
| Medium | API client error handling (401, 500, network) | Unit |
| Low | Chart rendering with various data shapes | Visual regression |
| Low | Responsive breakpoints | Manual / Playwright |
