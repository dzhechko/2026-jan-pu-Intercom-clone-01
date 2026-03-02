# Pseudocode -- Web Chat Widget

## initWidget(config)

```
FUNCTION initWidget(config):
  MERGE defaults (position="bottom-right", greeting=Russian text) over config
  CREATE WidgetApi(apiKey, apiUrl)
  sessionId = getOrCreateSessionId()
  CREATE <div id="cloudru-chat-widget"> with closed ShadowRoot
  INJECT WIDGET_CSS into shadow, APPEND host to document.body
  CALL render(), startProactiveTimer()
```

## getOrCreateSessionId()

```
FUNCTION getOrCreateSessionId():
  sid = localStorage.getItem("cloudru_widget_session")
  IF null: sid = crypto.randomUUID() ?? timestamp+random fallback
           localStorage.setItem(key, sid)
  RETURN sid
```

## createConversation(sessionId)

```
FUNCTION createConversation(sessionId):
  POST /api/v1/conversations
    HEADERS: X-API-Key: apiKey
    BODY: { channel: "web_widget", channel_user_id: sessionId }
  RETURN { id, status, channel, created_at }
```

## sendMessage(text)

```
FUNCTION sendMessage(text):
  PUSH { role: "user", content: text } to messages[]
  SET isSending=true, INCREMENT messageCount, render()
  TRY:
    IF conversationId null: conversationId = (AWAIT createConversation()).id
    result = AWAIT api.sendMessage(conversationId, text)
    CALL handleAssistantResponse(result.assistant_response)
  CATCH: PUSH error fallback message to messages[]
  FINALLY: isSending=false, render()
```

## handleAssistantResponse(response)

```
FUNCTION handleAssistantResponse(response):
  PUSH { role: "assistant", content, agentType, sources } to messages[]
  IF messageCount >= 5 AND confidence > 0.7
     AND any message agentType in (architect, cost_calculator):
    SET showLeadForm = true
```

## renderMessage(msg)

```
FUNCTION renderMessage(msg):
  CREATE <div class="msg {role}">
  IF assistant AND agentType: PREPEND agent-badge with localized label
  APPEND escapeHtml(content)
  IF sources[]: APPEND <div class="sources"> with <a> links
```

## injectStyles() and render()

```
FUNCTION injectStyles():
  CREATE <style>, textContent = WIDGET_CSS, APPEND to ShadowRoot
  // :host{all:initial}, .widget-bubble, .widget-panel(380x520),
  // @media max-480px (full-screen), .typing animation, .lead-form
FUNCTION render():
  CLEAR shadow children (preserve <style>), renderBubble()
  IF isOpen: renderPanel() -> header, messages, typing, lead form, input, footer
  SCROLL to bottom, FOCUS textarea
```
