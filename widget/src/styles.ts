/** Embedded CSS for the chat widget (injected into Shadow DOM). */
export const WIDGET_CSS = `
:host {
  all: initial;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #1a1a1a;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Chat bubble */
.widget-bubble {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 999999;
}

.widget-bubble:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
}

.widget-bubble svg {
  width: 24px;
  height: 24px;
  fill: currentColor;
}

.widget-bubble .badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ef4444;
  color: white;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Proactive message */
.proactive {
  position: fixed;
  bottom: 90px;
  right: 24px;
  background: white;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  max-width: 280px;
  font-size: 13px;
  color: #374151;
  cursor: pointer;
  animation: slideIn 0.3s ease-out;
  z-index: 999998;
}

.proactive .close-proactive {
  position: absolute;
  top: 4px;
  right: 8px;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}

/* Chat panel */
.widget-panel {
  position: fixed;
  bottom: 90px;
  right: 24px;
  width: 380px;
  height: 520px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.16);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideIn 0.25s ease-out;
  z-index: 999999;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 480px) {
  .widget-panel {
    width: 100vw;
    height: 100vh;
    bottom: 0;
    right: 0;
    border-radius: 0;
  }
}

/* Header */
.panel-header {
  padding: 14px 16px;
  background: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.panel-header .title {
  font-size: 15px;
  font-weight: 600;
}

.panel-header .subtitle {
  font-size: 12px;
  opacity: 0.85;
}

.panel-header button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  opacity: 0.8;
  transition: opacity 0.15s;
}

.panel-header button:hover {
  opacity: 1;
}

/* Messages area */
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.messages::-webkit-scrollbar {
  width: 4px;
}

.messages::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

.msg {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.msg.user {
  align-self: flex-end;
  background: #2563eb;
  color: white;
  border-bottom-right-radius: 4px;
}

.msg.assistant {
  align-self: flex-start;
  background: #f3f4f6;
  color: #1f2937;
  border-bottom-left-radius: 4px;
}

.msg .agent-badge {
  font-size: 10px;
  color: #6b7280;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.msg .sources {
  margin-top: 8px;
  font-size: 11px;
  color: #6b7280;
}

.msg .sources a {
  color: #2563eb;
  text-decoration: none;
}

.msg .sources a:hover {
  text-decoration: underline;
}

/* Typing indicator */
.typing {
  align-self: flex-start;
  padding: 10px 14px;
  background: #f3f4f6;
  border-radius: 12px;
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing span {
  width: 6px;
  height: 6px;
  background: #9ca3af;
  border-radius: 50%;
  animation: bounce 1.4s infinite both;
}

.typing span:nth-child(2) { animation-delay: 0.16s; }
.typing span:nth-child(3) { animation-delay: 0.32s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

/* Input area */
.input-area {
  padding: 12px 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
  align-items: flex-end;
  flex-shrink: 0;
}

.input-area textarea {
  flex: 1;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 13px;
  font-family: inherit;
  resize: none;
  min-height: 36px;
  max-height: 100px;
  outline: none;
  transition: border-color 0.15s;
}

.input-area textarea:focus {
  border-color: #2563eb;
}

.input-area .send-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.15s;
}

.input-area .send-btn:hover {
  background: #1d4ed8;
}

.input-area .send-btn:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.input-area .send-btn svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
}

/* Footer */
.panel-footer {
  padding: 8px 16px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: #9ca3af;
  flex-shrink: 0;
}

.panel-footer button {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  font-size: 11px;
  text-decoration: underline;
}

.panel-footer button:hover {
  color: #2563eb;
}

/* Lead capture form */
.lead-form {
  padding: 16px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.lead-form h3 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #1f2937;
}

.lead-form input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 13px;
  font-family: inherit;
  margin-bottom: 8px;
  outline: none;
}

.lead-form input:focus {
  border-color: #2563eb;
}

.lead-form .form-actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.lead-form .submit-btn {
  flex: 1;
  padding: 8px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
}

.lead-form .submit-btn:hover {
  background: #1d4ed8;
}

.lead-form .skip-btn {
  padding: 8px 12px;
  background: none;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 13px;
  color: #6b7280;
  cursor: pointer;
}
`;
