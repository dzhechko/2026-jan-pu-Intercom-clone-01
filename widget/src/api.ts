/** API client for the Cloud.ru AI Consultant widget. */

export interface WidgetConfig {
  apiKey: string;
  apiUrl: string;
  tenantId?: string;
}

export interface ConversationData {
  id: string;
  status: string;
  channel: string;
  created_at: string;
}

export interface Source {
  title: string;
  url: string;
}

export interface AssistantResponse {
  id: string;
  content: string;
  agent_type: string | null;
  confidence: number;
  sources: Source[];
  created_at: string;
}

export interface SendMessageResult {
  user_message: { id: string; content: string; role: string; created_at: string };
  assistant_response: AssistantResponse;
  response_time_ms: number;
}

export class WidgetApi {
  private apiUrl: string;
  private apiKey: string;

  constructor(config: WidgetConfig) {
    this.apiUrl = config.apiUrl.replace(/\/+$/, "");
    this.apiKey = config.apiKey;
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.apiUrl}${path}`;
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": this.apiKey,
        ...options.headers,
      },
    });

    if (!res.ok) {
      const body = await res.text().catch(() => "");
      throw new Error(`API ${res.status}: ${body}`);
    }

    return res.json();
  }

  async createConversation(
    channelUserId: string,
    initialMessage?: string,
  ): Promise<ConversationData> {
    return this.request<ConversationData>("/api/v1/conversations", {
      method: "POST",
      body: JSON.stringify({
        channel: "web_widget",
        channel_user_id: channelUserId,
        initial_message: initialMessage || null,
      }),
    });
  }

  async sendMessage(conversationId: string, content: string): Promise<SendMessageResult> {
    return this.request<SendMessageResult>(
      `/api/v1/conversations/${conversationId}/messages`,
      {
        method: "POST",
        body: JSON.stringify({ content, role: "user" }),
      },
    );
  }
}
