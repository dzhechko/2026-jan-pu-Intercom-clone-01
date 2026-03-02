/**
 * Cloud.ru AI Consultant — Embeddable Chat Widget
 *
 * Usage:
 *   <script>
 *     window.CHATWIDGET_CONFIG = {
 *       apiKey: 'YOUR_API_KEY',
 *       apiUrl: 'https://api.cloud-ru-ai.ru',
 *       greeting: 'Здравствуйте! Я AI-консультант Cloud.ru. Чем могу помочь?',
 *       proactive: {
 *         enabled: true,
 *         delayMs: 60000,
 *         message: 'Нужна помощь с расчётом стоимости?',
 *       },
 *     };
 *   </script>
 *   <script src="https://cdn.cloud-ru-ai.ru/widget.js" async defer></script>
 */

import { WIDGET_CSS } from "./styles";
import { WidgetApi, type AssistantResponse, type Source } from "./api";

// ─── Types ──────────────────────────────────────────────────────────────────

interface ChatWidgetConfig {
  apiKey: string;
  apiUrl: string;
  tenantId?: string;
  position?: "bottom-right" | "bottom-left";
  greeting?: string;
  proactive?: {
    enabled: boolean;
    delayMs?: number;
    message?: string;
  };
  theme?: {
    primaryColor?: string;
    headerTitle?: string;
  };
}

interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
  agentType?: string | null;
  sources?: Source[];
}

// ─── SVG Icons ──────────────────────────────────────────────────────────────

const ICON_CHAT = `<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>`;
const ICON_CLOSE = `<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>`;
const ICON_SEND = `<svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>`;

// ─── Widget Class ───────────────────────────────────────────────────────────

class ChatWidget {
  private config: ChatWidgetConfig;
  private api: WidgetApi;
  private host: HTMLElement;
  private shadow: ShadowRoot;
  private conversationId: string | null = null;
  private sessionId: string;
  private messages: ChatMessage[] = [];
  private isOpen = false;
  private isSending = false;
  private showLeadForm = false;
  private proactiveTimer: ReturnType<typeof setTimeout> | null = null;
  private proactiveDismissed = false;
  private messageCount = 0;

  constructor(config: ChatWidgetConfig) {
    this.config = {
      position: "bottom-right",
      greeting: "Здравствуйте! Я AI-консультант Cloud.ru. Чем могу помочь?",
      ...config,
    };

    this.api = new WidgetApi({ apiKey: config.apiKey, apiUrl: config.apiUrl });
    this.sessionId = this.getOrCreateSessionId();

    // Create Shadow DOM host
    this.host = document.createElement("div");
    this.host.id = "cloudru-chat-widget";
    this.shadow = this.host.attachShadow({ mode: "closed" });

    // Inject styles
    const style = document.createElement("style");
    style.textContent = WIDGET_CSS;
    this.shadow.appendChild(style);

    document.body.appendChild(this.host);

    this.render();
    this.startProactiveTimer();
  }

  private getOrCreateSessionId(): string {
    const key = "cloudru_widget_session";
    let sid = localStorage.getItem(key);
    if (!sid) {
      sid = crypto.randomUUID?.() ?? `s_${Date.now()}_${Math.random().toString(36).slice(2)}`;
      localStorage.setItem(key, sid);
    }
    return sid;
  }

  // ─── Rendering ────────────────────────────────────────────────────────

  private render(): void {
    // Clear existing content (keep <style>)
    const style = this.shadow.querySelector("style")!;
    while (this.shadow.lastChild && this.shadow.lastChild !== style) {
      this.shadow.removeChild(this.shadow.lastChild);
    }

    // Render bubble
    this.renderBubble();

    // Render proactive message
    if (!this.isOpen && !this.proactiveDismissed && this.config.proactive?.enabled) {
      // Proactive is handled by timer → renderProactive()
    }

    // Render panel
    if (this.isOpen) {
      this.renderPanel();
    }
  }

  private renderBubble(): void {
    const btn = document.createElement("button");
    btn.className = "widget-bubble";
    if (this.config.position === "bottom-left") {
      btn.style.left = "24px";
      btn.style.right = "auto";
    }
    btn.innerHTML = this.isOpen ? ICON_CLOSE : ICON_CHAT;
    btn.addEventListener("click", () => this.toggle());
    this.shadow.appendChild(btn);
  }

  private renderProactive(): void {
    // Remove existing proactive
    this.shadow.querySelector(".proactive")?.remove();

    if (this.isOpen || this.proactiveDismissed) return;

    const msg = this.config.proactive?.message || "Нужна помощь с расчётом стоимости?";
    const div = document.createElement("div");
    div.className = "proactive";
    if (this.config.position === "bottom-left") {
      div.style.left = "24px";
      div.style.right = "auto";
    }
    div.innerHTML = `
      <button class="close-proactive">&times;</button>
      ${this.escapeHtml(msg)}
    `;
    div.querySelector(".close-proactive")!.addEventListener("click", (e) => {
      e.stopPropagation();
      this.proactiveDismissed = true;
      div.remove();
    });
    div.addEventListener("click", () => {
      this.proactiveDismissed = true;
      div.remove();
      this.open();
    });
    this.shadow.appendChild(div);
  }

  private renderPanel(): void {
    const panel = document.createElement("div");
    panel.className = "widget-panel";
    if (this.config.position === "bottom-left") {
      panel.style.left = "24px";
      panel.style.right = "auto";
    }

    // Header
    const header = document.createElement("div");
    header.className = "panel-header";
    header.innerHTML = `
      <div>
        <div class="title">${this.escapeHtml(this.config.theme?.headerTitle || "Cloud.ru Assistant")}</div>
        <div class="subtitle">AI-консультант</div>
      </div>
      <button aria-label="Close">${ICON_CLOSE}</button>
    `;
    header.querySelector("button")!.addEventListener("click", () => this.close());
    panel.appendChild(header);

    // Messages
    const messagesDiv = document.createElement("div");
    messagesDiv.className = "messages";

    for (const msg of this.messages) {
      const el = document.createElement("div");
      el.className = `msg ${msg.role}`;

      let html = "";
      if (msg.role === "assistant" && msg.agentType) {
        const label = this.agentLabel(msg.agentType);
        html += `<div class="agent-badge">${this.escapeHtml(label)}</div>`;
      }
      html += this.escapeHtml(msg.content);

      if (msg.sources && msg.sources.length > 0) {
        html += `<div class="sources">`;
        for (const s of msg.sources) {
          if (s.url) {
            html += `<a href="${this.escapeHtml(s.url)}" target="_blank" rel="noopener">${this.escapeHtml(s.title)}</a> `;
          } else {
            html += `${this.escapeHtml(s.title)} `;
          }
        }
        html += `</div>`;
      }

      el.innerHTML = html;
      messagesDiv.appendChild(el);
    }

    // Typing indicator
    if (this.isSending) {
      const typing = document.createElement("div");
      typing.className = "typing";
      typing.innerHTML = `<span></span><span></span><span></span>`;
      messagesDiv.appendChild(typing);
    }

    panel.appendChild(messagesDiv);

    // Lead capture form
    if (this.showLeadForm) {
      panel.appendChild(this.renderLeadForm());
    }

    // Input area
    const inputArea = document.createElement("div");
    inputArea.className = "input-area";

    const textarea = document.createElement("textarea");
    textarea.placeholder = "Введите сообщение...";
    textarea.rows = 1;
    textarea.maxLength = 4000;
    textarea.addEventListener("input", () => {
      textarea.style.height = "auto";
      textarea.style.height = Math.min(textarea.scrollHeight, 100) + "px";
      sendBtn.disabled = !textarea.value.trim() || this.isSending;
    });
    textarea.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (textarea.value.trim() && !this.isSending) {
          this.sendMessage(textarea.value.trim());
        }
      }
    });

    const sendBtn = document.createElement("button");
    sendBtn.className = "send-btn";
    sendBtn.disabled = true;
    sendBtn.innerHTML = ICON_SEND;
    sendBtn.addEventListener("click", () => {
      if (textarea.value.trim() && !this.isSending) {
        this.sendMessage(textarea.value.trim());
      }
    });

    inputArea.appendChild(textarea);
    inputArea.appendChild(sendBtn);
    panel.appendChild(inputArea);

    // Footer
    const footer = document.createElement("div");
    footer.className = "panel-footer";
    footer.innerHTML = `
      <span>Powered by AI-Консультант</span>
      <button class="escalate-btn">Связаться с экспертом</button>
    `;
    footer.querySelector(".escalate-btn")!.addEventListener("click", () => {
      this.sendMessage("Хочу поговорить со специалистом");
    });
    panel.appendChild(footer);

    this.shadow.appendChild(panel);

    // Scroll to bottom and focus
    requestAnimationFrame(() => {
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
      textarea.focus();
    });
  }

  private renderLeadForm(): HTMLElement {
    const form = document.createElement("div");
    form.className = "lead-form";
    form.innerHTML = `
      <h3>Оставьте контакты для связи</h3>
      <input type="text" name="name" placeholder="Имя *" required />
      <input type="text" name="company" placeholder="Компания *" required />
      <input type="email" name="email" placeholder="Email *" required />
      <input type="tel" name="phone" placeholder="Телефон (необязательно)" />
      <div class="form-actions">
        <button class="submit-btn">Отправить</button>
        <button class="skip-btn">Пропустить</button>
      </div>
    `;

    form.querySelector(".submit-btn")!.addEventListener("click", () => {
      const name = (form.querySelector('[name="name"]') as HTMLInputElement).value;
      const company = (form.querySelector('[name="company"]') as HTMLInputElement).value;
      const email = (form.querySelector('[name="email"]') as HTMLInputElement).value;
      const phone = (form.querySelector('[name="phone"]') as HTMLInputElement).value;

      if (!name || !company || !email) return;

      // Send contact info as a message for the orchestrator to process
      const contactMsg = `Мои контакты: ${name}, ${company}, ${email}${phone ? `, ${phone}` : ""}`;
      this.showLeadForm = false;
      this.sendMessage(contactMsg);
    });

    form.querySelector(".skip-btn")!.addEventListener("click", () => {
      this.showLeadForm = false;
      this.render();
    });

    return form;
  }

  // ─── Actions ──────────────────────────────────────────────────────────

  private toggle(): void {
    this.isOpen ? this.close() : this.open();
  }

  private open(): void {
    this.isOpen = true;
    this.proactiveDismissed = true;
    this.shadow.querySelector(".proactive")?.remove();

    // Add greeting if first open
    if (this.messages.length === 0 && this.config.greeting) {
      this.messages.push({
        role: "assistant",
        content: this.config.greeting,
        agentType: null,
      });
    }

    this.render();
  }

  private close(): void {
    this.isOpen = false;
    this.render();
  }

  private async sendMessage(text: string): Promise<void> {
    // Add user message
    this.messages.push({ role: "user", content: text });
    this.isSending = true;
    this.messageCount++;
    this.render();

    try {
      // Create conversation if needed (without initial_message to avoid double processing)
      if (!this.conversationId) {
        const conv = await this.api.createConversation(this.sessionId);
        this.conversationId = conv.id;
      }

      const result = await this.api.sendMessage(this.conversationId, text);
      this.handleAssistantResponse(result.assistant_response);
    } catch (err) {
      this.messages.push({
        role: "assistant",
        content: "Извините, произошла ошибка. Попробуйте ещё раз.",
      });
    } finally {
      this.isSending = false;
      this.render();
    }
  }

  private handleAssistantResponse(response: AssistantResponse): void {
    this.messages.push({
      role: "assistant",
      content: response.content,
      agentType: response.agent_type,
      sources: response.sources,
    });

    // Check if we should show lead capture (after 5+ messages with high-value intents)
    if (this.messageCount >= 5 && !this.showLeadForm && response.confidence > 0.7) {
      const hasArchitect = this.messages.some((m) => m.agentType === "architect");
      const hasCost = this.messages.some((m) => m.agentType === "cost_calculator");
      if (hasArchitect || hasCost) {
        this.showLeadForm = true;
      }
    }
  }

  private startProactiveTimer(): void {
    if (!this.config.proactive?.enabled) return;
    const delay = this.config.proactive.delayMs ?? 60000;
    this.proactiveTimer = setTimeout(() => {
      if (!this.isOpen && !this.proactiveDismissed) {
        this.renderProactive();
      }
    }, delay);
  }

  // ─── Helpers ──────────────────────────────────────────────────────────

  private escapeHtml(text: string): string {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  private agentLabel(agentType: string): string {
    const labels: Record<string, string> = {
      architect: "Архитектор",
      cost_calculator: "Калькулятор",
      compliance: "Комплаенс",
      migration: "Миграция",
      ai_factory: "AI Factory",
      human_escalation: "Эскалация",
    };
    return labels[agentType] || agentType;
  }

  destroy(): void {
    if (this.proactiveTimer) clearTimeout(this.proactiveTimer);
    this.host.remove();
  }
}

// ─── Auto-init from global config ───────────────────────────────────────────

declare global {
  interface Window {
    CHATWIDGET_CONFIG?: ChatWidgetConfig;
    CloudRuWidget?: {
      init: (config: ChatWidgetConfig) => ChatWidget;
    };
  }
}

function init(config: ChatWidgetConfig): ChatWidget {
  return new ChatWidget(config);
}

// Export for programmatic use
if (typeof window !== "undefined") {
  window.CloudRuWidget = { init };

  // Auto-init if config is present
  if (window.CHATWIDGET_CONFIG) {
    document.addEventListener("DOMContentLoaded", () => {
      if (window.CHATWIDGET_CONFIG) {
        init(window.CHATWIDGET_CONFIG);
      }
    });
  }
}

export { ChatWidget, init };
export type { ChatWidgetConfig };
