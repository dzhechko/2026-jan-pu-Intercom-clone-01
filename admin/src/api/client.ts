const API_BASE = "/api/v1";

function getToken(): string | null {
  return localStorage.getItem("token");
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers as Record<string, string> || {}),
  };

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export const api = {
  login: (email: string, password: string) =>
    request<{ access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  getMetrics: (period: string = "7d") =>
    request<import("../types").IMetrics>(`/dashboard/metrics?period=${period}`),

  getConversations: (page: number = 1, limit: number = 20) =>
    request<{ items: import("../types").IConversation[]; total: number }>(
      `/dashboard/conversations?page=${page}&limit=${limit}`,
    ),

  getConversation: (id: string) =>
    request<import("../types").IConversation & { messages: import("../types").IMessage[] }>(
      `/conversations/${id}`,
    ),

  getLeads: (page: number = 1) =>
    request<{ items: import("../types").ILead[]; total: number }>(
      `/dashboard/leads?page=${page}`,
    ),

  getRoiMetrics: (period: string = "30d") =>
    request<import("../types").IRoiMetrics>(`/dashboard/roi?period=${period}`),
};
