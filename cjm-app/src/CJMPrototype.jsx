/**
 * CJM Prototype: Hybrid B+D — "Open Agentic Platform"
 *
 * Combines:
 *   Variant B: Developer-First Open Core (install in 5 min, self-hosted, BYO LLM)
 *   Variant D: Agentic Platform 2026 (AI actions via MCP, multi-agent, voice AI)
 *
 * Company: Intercom Clone
 * Geography: Global (EN)
 * Industry: Customer Communication / AI Support
 * Generated: 2026-03-02
 *
 * Sources are embedded as SOURCES object with clickable links.
 */

import React, { useState, useCallback } from "react";

// ============================================================
// SOURCES — all micro-trend references with clickable URLs
// ============================================================
const SOURCES = {
  agentic_market: {
    fact: "AI Agent market: $7.84B (2025) → $52.62B (2030), CAGR 46.3%",
    url: "https://www.index.dev/blog/ai-agents-statistics",
    publisher: "Index.dev",
  },
  gartner_80pct: {
    fact: "80% of customer service issues resolved autonomously by 2029",
    url: "https://www.gartner.com/en/newsroom/press-releases/2025-03-05-gartner-predicts-agentic-ai-will-autonomously-resolve-80-percent-of-common-customer-service-issues-without-human-intervention-by-20290",
    publisher: "Gartner",
  },
  multi_agent_surge: {
    fact: "Multi-agent system inquiries surged 1,445% in one year",
    url: "https://www.gartner.com/en/newsroom/press-releases/2025-03-05-gartner-predicts-agentic-ai-will-autonomously-resolve-80-percent-of-common-customer-service-issues-without-human-intervention-by-20290",
    publisher: "Gartner",
  },
  mcp_adoption: {
    fact: "MCP: 97M+ monthly SDK downloads, adopted by Anthropic, OpenAI, Google, Microsoft",
    url: "https://www.cdata.com/blog/2026-year-enterprise-ready-mcp-adoption",
    publisher: "CData",
  },
  mcp_support: {
    fact: "MCP for AI-Powered Customer Support — universal standard",
    url: "https://www.searchunify.com/resource-center/sudo-technical-blogs/model-context-protocol-the-future-of-ai-in-customer-support-2025/",
    publisher: "SearchUnify",
  },
  conv_commerce_market: {
    fact: "Conversational Commerce: $11.26B (2025) → $20.28B (2030), CAGR 12.47%",
    url: "https://www.mordorintelligence.com/industry-reports/conversational-commerce-market",
    publisher: "Mordor Intelligence",
  },
  conv_commerce_ready: {
    fact: "66% of consumers ready to buy via messaging, 4x conversion vs websites",
    url: "https://www.bigcommerce.com/articles/ecommerce/conversational-commerce/",
    publisher: "BigCommerce",
  },
  conv_commerce_stats: {
    fact: "Chatbot websites see +23% conversion boost",
    url: "https://bigsur.ai/blog/conversational-commerce-statistics",
    publisher: "BigSur AI",
  },
  voice_ai_market: {
    fact: "Voice AI market projected $47.5B by 2034, CAGR 22.7%",
    url: "https://www.retellai.com/blog/best-voice-ai-agent-platforms",
    publisher: "Retell AI",
  },
  gdpr_fines: {
    fact: "GDPR fines: EUR 2.3B in 2025 alone (+38% YoY), EUR 6.7B+ total",
    url: "https://secureprivacy.ai/blog/data-privacy-trends-2026",
    publisher: "SecurePrivacy",
  },
  eu_ai_act: {
    fact: "EU AI Act fully applicable August 2, 2026",
    url: "https://secureprivacy.ai/blog/privacy-laws-2026",
    publisher: "SecurePrivacy",
  },
  chatwoot_oss: {
    fact: "Chatwoot: 23.8K+ GitHub stars, YC-backed, leading open-source Intercom alternative",
    url: "https://github.com/chatwoot/chatwoot",
    publisher: "GitHub",
  },
  copilot_roi: {
    fact: "90% of CX leaders report positive ROI from AI copilots",
    url: "https://www.assembled.com/blog/ai-copilots-customer-support",
    publisher: "Assembled",
  },
  auto_qa: {
    fact: "Auto QA scores 100% of interactions with evidence-based evaluation",
    url: "https://www.observe.ai/post-interaction/auto-qa",
    publisher: "Observe.AI",
  },
  whatsapp_calling: {
    fact: "WhatsApp Business Calling API launched Dec 2025 — voice + video in business threads",
    url: "https://mobileecosystemforum.com/2025/12/17/whatsapp-opens-a-new-front-in-business-voice-with-calling-api/",
    publisher: "MEF",
  },
  self_service: {
    fact: "92% of users would use an online knowledge base; AI KB reduces tickets 30-50%",
    url: "https://www.usepylon.com/blog/best-b2b-knowledge-base-software-ai-powered-platforms-2025",
    publisher: "Pylon",
  },
  proactive_support: {
    fact: "Predictive support: 20-30% efficiency gain, 87% welcome proactive outreach",
    url: "https://medium.com/@devashish_m/predictive-analytics-for-proactive-customer-support-in-2025-54e432015db4",
    publisher: "McKinsey / Medium",
  },
  agentic_cx: {
    fact: "56% of support interactions will use agentic AI by mid-2026",
    url: "https://www.searchunify.com/resource-center/blog/agentic-ai-in-customer-support-a-2026-data-driven-deep-dive",
    publisher: "SearchUnify",
  },
  oss_alternatives: {
    fact: "Open-source Intercom alternatives gaining traction: cost, sovereignty, customization",
    url: "https://blog.octabyte.io/posts/open-source-alternatives-to-intercom/",
    publisher: "OctaByte",
  },
  zero_party_data: {
    fact: "Zero-party data and consent-first design becoming the privacy standard",
    url: "https://secureprivacy.ai/blog/zero-party-data-in-consent-management",
    publisher: "SecurePrivacy",
  },
  conversational_ai_market: {
    fact: "Conversational AI market: $12.24B (2024) → $61.69B (2032)",
    url: "https://masterofcode.com/blog/conversational-ai-trends",
    publisher: "MasterOfCode",
  },
};

// ============================================================
// CJM VARIANT DATA: Hybrid B+D
// ============================================================
const VARIANT = {
  id: "BD",
  name: "Open Agentic Platform",
  emoji: "🚀",
  colors: {
    primary: "#6366F1",    // indigo-500
    secondary: "#8B5CF6",  // violet-500
    accent: "#06B6D4",     // cyan-500
    success: "#10B981",    // emerald-500
    warning: "#F59E0B",    // amber-500
    danger: "#EF4444",     // red-500
    bg: "#0F172A",         // slate-900
    bgLight: "#1E293B",    // slate-800
    bgCard: "#334155",     // slate-700
    text: "#F8FAFC",       // slate-50
    textMuted: "#94A3B8",  // slate-400
  },

  landing: {
    headline: "AI Agents That ACT. Not Just Chat.",
    subheadline: "Open-source agentic support platform. Self-hosted. BYO LLM. MCP-native.",
    cta_primary: "Deploy Self-Hosted (Free)",
    cta_secondary: "Try Cloud Free",
    cta_github: "Star on GitHub",
    demo: {
      old_label: "Typical AI Chatbot",
      old_response: '"Here are the instructions for a refund: go to Settings > Billing > ..."',
      new_label: "Our AI Agent",
      new_steps: [
        "Checked order #4821 via Stripe MCP",
        "Created refund request ($49.00)",
        "Processed refund to card •••4242",
        "Notified customer via email",
      ],
      old_result: "Customer does everything manually. 😤",
      new_result: "Done. 3 seconds. Zero human effort. 🎯",
    },
    badges: ["Open Source", "Self-Hosted", "BYO LLM", "MCP-Native", "Voice AI"],
    sources: ["agentic_market", "gartner_80pct"],
  },

  onboarding: {
    steps: [
      {
        title: "Install & Run",
        type: "code",
        content: [
          "npx create-agentic-support my-support",
          "cd my-support",
          "docker compose up",
          "# ✅ Running on http://localhost:3000",
        ],
        alt: "Or: one-click deploy to cloud",
        time: "2 min",
      },
      {
        title: "Connect Knowledge Sources",
        type: "integrations",
        options: ["Docs URL", "Notion", "Confluence", "GitHub Wiki", "Upload .md"],
        time: "3 min",
      },
      {
        title: "Connect Actions via MCP",
        type: "mcp",
        servers: [
          { name: "Stripe", actions: "refunds, subscriptions, invoices", icon: "💳" },
          { name: "Jira", actions: "create tickets, update status", icon: "📋" },
          { name: "Database", actions: "read customer data, update records", icon: "🗄️" },
          { name: "Email", actions: "send notifications, campaigns", icon: "📧" },
          { name: "Custom", actions: "add your own MCP server", icon: "🔧" },
        ],
        sources: ["mcp_adoption", "mcp_support"],
        time: "5 min",
      },
      {
        title: "Configure Channels",
        type: "channels",
        options: [
          { name: "Chat Widget", status: "auto", icon: "💬" },
          { name: "Email", status: "auto", icon: "📧" },
          { name: "WhatsApp", status: "connect", icon: "📱", source: "whatsapp_calling" },
          { name: "Voice AI", status: "connect", icon: "🎙️", source: "voice_ai_market" },
          { name: "Telegram", status: "connect", icon: "✈️" },
          { name: "Slack", status: "connect", icon: "💼" },
        ],
        time: "3 min",
      },
      {
        title: "Test Drive Your Agent",
        type: "simulation",
        scenario: {
          customer_message: "I want to return order #4821, the item arrived damaged",
          agent_steps: [
            { action: "Checking order #4821 in database...", tool: "Database MCP", time: "0.3s" },
            { action: "Order found: Blue Widget, $49.00, delivered 2 days ago", tool: "Database MCP", time: "0.1s" },
            { action: "Checking return policy: eligible (within 30 days)", tool: "Knowledge Base", time: "0.2s" },
            { action: "Initiating refund of $49.00 to card •••4242", tool: "Stripe MCP", time: "0.8s" },
            { action: "Refund processed ✅ Sending confirmation email", tool: "Email MCP", time: "0.4s" },
          ],
          total_time: "1.8s",
          result: "Customer receives: 'Your refund of $49.00 has been processed. You\\'ll see it in 3-5 business days.'",
        },
        time: "2 min",
      },
    ],
    total_time: "< 15 min",
    sources: ["agentic_cx"],
  },

  aha: {
    title: "The AI Didn't Just Answer — It DID The Thing",
    description: "The moment you see your AI agent autonomously execute a multi-step action (check order → verify policy → process refund → notify customer) — not just paste an FAQ link.",
    wow_metric: "1.8 seconds. 4 actions. Zero human effort.",
    kpi: "First autonomous action completed",
    validation_question: "Would you trust this AI agent to handle real customer requests with real money?",
    sources: ["gartner_80pct", "agentic_market"],
  },

  dashboard: {
    name: "Command Center",
    sections: {
      multi_agent_hub: {
        title: "Multi-Agent Hub",
        agents: [
          { name: "Triage Agent", role: "Routes & prioritizes", status: "auto" },
          { name: "Billing Agent", role: "Stripe actions", status: "auto" },
          { name: "Technical Agent", role: "Jira + DB actions", status: "auto" },
          { name: "Commerce Agent", role: "Product recs + checkout", status: "optional" },
          { name: "Human Escalation", role: "Fallback to team", status: "always" },
        ],
        source: "multi_agent_surge",
      },
      live_conversation: {
        title: "Live Conversation",
        example: {
          customer: "My payment failed and my subscription was cancelled",
          agent_name: "Billing Agent",
          steps: [
            "Checked Stripe: card_declined (insufficient_funds)",
            "Restored subscription to active state",
            "Sent new payment link via email",
            "Response: 'All restored! Here\\'s a fresh payment link: ...'",
          ],
        },
      },
      copilot_panel: {
        title: "AI Copilot",
        features: [
          { name: "Suggested Reply", icon: "💡", description: "AI-drafted response from KB + context" },
          { name: "Sentiment", icon: "😠→😊", description: "Real-time emotion tracking" },
          { name: "QA Score", icon: "📊", description: "Auto-scored 94/100", source: "auto_qa" },
          { name: "Similar Cases", icon: "📈", description: "23 similar cases this week" },
        ],
        source: "copilot_roi",
      },
      analytics: {
        metrics: [
          { label: "AI Resolved", value: "847/1,021", pct: "83%" },
          { label: "Avg Resolution", value: "12 sec" },
          { label: "CSAT", value: "94%" },
          { label: "Cost per Resolution", value: "$0.31" },
          { label: "Actions Executed", value: "2,340" },
          { label: "Monthly Savings", value: "$12,400" },
          { label: "Voice Calls Handled", value: "89" },
          { label: "Active Channels", value: "6" },
        ],
      },
    },
    sources: ["copilot_roi", "auto_qa", "multi_agent_surge"],
  },

  paywall: {
    timing: "After Aha moment — user sees AI execute real action, then converts",
    plans: {
      self_hosted: {
        name: "Self-Hosted",
        price: "FREE",
        period: "forever",
        tagline: "Your data, your servers, your control",
        features: [
          "Full platform (all features)",
          "Unlimited conversations",
          "Unlimited agents",
          "BYO LLM key (pay your provider directly)",
          "Docker Compose / Kubernetes",
          "Community support",
          "GDPR: full data control",
        ],
        cta: "docker compose up",
        sources: ["gdpr_fines", "chatwoot_oss"],
      },
      cloud_free: {
        name: "Cloud Free",
        price: "$0",
        period: "/month",
        tagline: "Get started in 30 seconds",
        features: [
          "100 AI resolutions/month",
          "1 agent seat",
          "2 channels (widget + email)",
          "Basic knowledge base",
          "Community support",
        ],
        cta: "Start Free",
      },
      cloud_starter: {
        name: "Starter",
        price: "$0.49",
        period: "/resolution",
        tagline: "Pay only when AI resolves. No seat fees.",
        features: [
          "Unlimited AI resolutions",
          "3 agent seats included",
          "All channels",
          "MCP integrations (5 servers)",
          "AI Copilot for agents",
          "Basic analytics",
          "Email support",
        ],
        cta: "Start Starter",
        comparison: "Intercom: $29/seat + $0.99/resolution = 2x more expensive",
      },
      cloud_team: {
        name: "Team",
        price: "$39",
        period: "/seat/month",
        tagline: "For growing support teams",
        features: [
          "Everything in Starter",
          "$0.29/resolution (volume discount)",
          "Unlimited agent seats",
          "Multi-agent orchestration",
          "Voice AI channel",
          "Conversational commerce",
          "Auto QA (100% scoring)",
          "Advanced analytics + API",
          "Priority support",
        ],
        cta: "Start Team Trial",
        sources: ["voice_ai_market", "conv_commerce_market"],
      },
      cloud_scale: {
        name: "Scale",
        price: "$99",
        period: "/seat/month",
        tagline: "Enterprise-ready, compliance-included",
        features: [
          "Everything in Team",
          "Unlimited AI resolutions included",
          "SSO / SAML",
          "HIPAA compliance",
          "SLA guarantee (99.9%)",
          "Custom AI model training",
          "Dedicated infrastructure",
          "EU data residency",
          "EU AI Act compliance toolkit",
        ],
        cta: "Contact Sales",
        sources: ["eu_ai_act", "gdpr_fines"],
      },
    },
  },

  invite: {
    hook: "Connect another channel",
    mechanics: [
      { trigger: "After first AI resolution", action: "Add WhatsApp channel" },
      { trigger: "After 10 resolutions", action: "Invite a teammate" },
      { trigger: "After team onboarding", action: "Enable Voice AI" },
      { trigger: "Happy customer", action: "Star on GitHub / Share on Twitter" },
    ],
    viral_loop: "Developer installs → AI resolves → shares on HN/Twitter → more devs install",
    source: "oss_alternatives",
  },

  commerce: {
    title: "Conversational Commerce (Expansion Module)",
    example: {
      customer: "I want the same shirt but in blue, size M",
      agent_steps: [
        { action: "Found: Blue Classic Tee, Size M — $29.99", type: "product_card" },
        { action: "[Add to Cart] [Pay in Chat — Stripe]", type: "checkout" },
        { action: "Payment accepted ✅ Tracking: #TRK-8841", type: "confirmation" },
      ],
    },
    sources: ["conv_commerce_market", "conv_commerce_ready", "conv_commerce_stats"],
  },
};

// ============================================================
// CJM METADATA — standard stages (AARRR framework)
// ============================================================
const CJM_META = {
  landing: {
    stage: "Acquisition",
    aarrr: "A — Acquisition",
    question: "Does the headline speak to a real pain? Would you click CTA?",
    metric: "Visitor → Signup conversion",
  },
  onboarding: {
    stage: "Activation",
    aarrr: "A — Activation",
    question: "Can you complete setup in <15 min? Where did you get stuck?",
    metric: "Signup → First AI Resolution",
  },
  aha: {
    stage: "Aha Moment",
    aarrr: "A — Activation (peak)",
    question: "Did the AI action surprise you? Would you trust it with real operations?",
    metric: "First autonomous action completed",
  },
  dashboard: {
    stage: "Engagement",
    aarrr: "R — Retention",
    question: "Would you check this dashboard daily? What's missing?",
    metric: "DAU/MAU, sessions/week",
  },
  paywall: {
    stage: "Monetization",
    aarrr: "R — Revenue",
    question: "Is the pricing clear? Would you pay $0.49/resolution?",
    metric: "Free → Paid conversion",
  },
  invite: {
    stage: "Referral",
    aarrr: "R — Referral",
    question: "Would you share this with a dev friend? Star on GitHub?",
    metric: "Invites sent, GitHub stars",
  },
};

// ============================================================
// SOURCE LINK COMPONENT
// ============================================================
function SourceLink({ id }) {
  const src = SOURCES[id];
  if (!src) return null;
  return (
    <a
      href={src.url}
      target="_blank"
      rel="noopener noreferrer"
      title={src.fact}
      style={{
        color: "#06B6D4",
        fontSize: "0.75rem",
        textDecoration: "underline",
        cursor: "pointer",
      }}
    >
      [{src.publisher}]
    </a>
  );
}

function SourceBadge({ id }) {
  const src = SOURCES[id];
  if (!src) return null;
  return (
    <div style={{ margin: "4px 0", padding: "4px 8px", background: "#1E293B", borderRadius: "4px", fontSize: "0.75rem", borderLeft: "3px solid #06B6D4" }}>
      <a href={src.url} target="_blank" rel="noopener noreferrer" style={{ color: "#06B6D4", textDecoration: "none" }}>
        📎 {src.fact}
      </a>
      <span style={{ color: "#94A3B8" }}> — {src.publisher}</span>
    </div>
  );
}

// ============================================================
// SCREEN COMPONENTS
// ============================================================

function LandingScreen() {
  const { landing } = VARIANT;
  return (
    <div style={{ background: VARIANT.colors.bg, color: VARIANT.colors.text, padding: "2rem", borderRadius: "12px" }}>
      <div style={{ textAlign: "center", marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "2.5rem", fontWeight: "800", background: `linear-gradient(135deg, ${VARIANT.colors.primary}, ${VARIANT.colors.accent})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
          {landing.headline}
        </h1>
        <p style={{ fontSize: "1.25rem", color: VARIANT.colors.textMuted, marginTop: "0.5rem" }}>
          {landing.subheadline}
        </p>
        <div style={{ display: "flex", gap: "1rem", justifyContent: "center", marginTop: "1.5rem" }}>
          <button style={{ background: VARIANT.colors.primary, color: "#fff", padding: "12px 24px", borderRadius: "8px", border: "none", fontWeight: "600", cursor: "pointer" }}>
            {landing.cta_primary}
          </button>
          <button style={{ background: "transparent", color: VARIANT.colors.primary, padding: "12px 24px", borderRadius: "8px", border: `2px solid ${VARIANT.colors.primary}`, fontWeight: "600", cursor: "pointer" }}>
            {landing.cta_secondary}
          </button>
          <button style={{ background: "transparent", color: VARIANT.colors.textMuted, padding: "12px 24px", borderRadius: "8px", border: `1px solid ${VARIANT.colors.bgCard}`, cursor: "pointer" }}>
            ⭐ {landing.cta_github}
          </button>
        </div>
      </div>

      {/* Demo: Old vs New */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginTop: "2rem" }}>
        <div style={{ background: VARIANT.colors.bgLight, padding: "1.5rem", borderRadius: "8px", border: `1px solid ${VARIANT.colors.danger}33` }}>
          <h3 style={{ color: VARIANT.colors.danger, marginBottom: "1rem" }}>❌ {landing.demo.old_label}</h3>
          <p style={{ fontStyle: "italic", color: VARIANT.colors.textMuted }}>{landing.demo.old_response}</p>
          <p style={{ marginTop: "1rem", color: VARIANT.colors.danger }}>{landing.demo.old_result}</p>
        </div>
        <div style={{ background: VARIANT.colors.bgLight, padding: "1.5rem", borderRadius: "8px", border: `1px solid ${VARIANT.colors.success}33` }}>
          <h3 style={{ color: VARIANT.colors.success, marginBottom: "1rem" }}>✅ {landing.demo.new_label}</h3>
          {landing.demo.new_steps.map((step, i) => (
            <p key={i} style={{ color: VARIANT.colors.success, margin: "4px 0" }}>✓ {step}</p>
          ))}
          <p style={{ marginTop: "1rem", fontWeight: "700", color: VARIANT.colors.success }}>{landing.demo.new_result}</p>
        </div>
      </div>

      {/* Badges */}
      <div style={{ display: "flex", gap: "0.5rem", justifyContent: "center", marginTop: "1.5rem", flexWrap: "wrap" }}>
        {landing.badges.map((badge) => (
          <span key={badge} style={{ padding: "4px 12px", background: VARIANT.colors.bgCard, borderRadius: "999px", fontSize: "0.85rem", color: VARIANT.colors.accent }}>
            {badge}
          </span>
        ))}
      </div>

      {/* Sources */}
      <div style={{ marginTop: "1.5rem" }}>
        {landing.sources.map((s) => <SourceBadge key={s} id={s} />)}
      </div>
    </div>
  );
}

function OnboardingScreen() {
  const { onboarding } = VARIANT;
  return (
    <div style={{ background: VARIANT.colors.bg, color: VARIANT.colors.text, padding: "2rem", borderRadius: "12px" }}>
      <h2 style={{ fontSize: "1.75rem", marginBottom: "0.5rem" }}>⚡ Setup in {onboarding.total_time}</h2>
      <p style={{ color: VARIANT.colors.textMuted, marginBottom: "2rem" }}>From zero to first AI resolution</p>

      {onboarding.steps.map((step, idx) => (
        <div key={idx} style={{ background: VARIANT.colors.bgLight, padding: "1.5rem", borderRadius: "8px", marginBottom: "1rem", borderLeft: `4px solid ${VARIANT.colors.primary}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h3 style={{ color: VARIANT.colors.accent }}>Step {idx + 1}: {step.title}</h3>
            <span style={{ color: VARIANT.colors.textMuted, fontSize: "0.85rem" }}>~{step.time}</span>
          </div>

          {step.type === "code" && (
            <pre style={{ background: VARIANT.colors.bg, padding: "1rem", borderRadius: "6px", marginTop: "0.75rem", fontSize: "0.9rem", color: VARIANT.colors.success, overflow: "auto" }}>
              {step.content.map((line, i) => <div key={i}>{line}</div>)}
            </pre>
          )}

          {step.type === "integrations" && (
            <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginTop: "0.75rem" }}>
              {step.options.map((opt) => (
                <span key={opt} style={{ padding: "6px 14px", background: VARIANT.colors.bgCard, borderRadius: "6px", fontSize: "0.85rem" }}>{opt}</span>
              ))}
            </div>
          )}

          {step.type === "mcp" && (
            <div style={{ marginTop: "0.75rem" }}>
              {step.servers.map((srv) => (
                <div key={srv.name} style={{ display: "flex", gap: "0.75rem", padding: "8px 0", borderBottom: `1px solid ${VARIANT.colors.bgCard}` }}>
                  <span>{srv.icon}</span>
                  <strong>{srv.name}</strong>
                  <span style={{ color: VARIANT.colors.textMuted }}>— {srv.actions}</span>
                </div>
              ))}
              {step.sources && step.sources.map((s) => <SourceBadge key={s} id={s} />)}
            </div>
          )}

          {step.type === "channels" && (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "0.5rem", marginTop: "0.75rem" }}>
              {step.options.map((ch) => (
                <div key={ch.name} style={{ display: "flex", alignItems: "center", gap: "0.5rem", padding: "8px 12px", background: VARIANT.colors.bgCard, borderRadius: "6px" }}>
                  <span>{ch.icon}</span>
                  <span>{ch.name}</span>
                  <span style={{ marginLeft: "auto", fontSize: "0.75rem", color: ch.status === "auto" ? VARIANT.colors.success : VARIANT.colors.textMuted }}>
                    {ch.status === "auto" ? "✅ auto" : "connect"}
                  </span>
                </div>
              ))}
            </div>
          )}

          {step.type === "simulation" && (
            <div style={{ marginTop: "0.75rem" }}>
              <div style={{ background: VARIANT.colors.bg, padding: "1rem", borderRadius: "6px" }}>
                <p style={{ color: VARIANT.colors.textMuted }}>Customer: <em>"{step.scenario.customer_message}"</em></p>
                <div style={{ marginTop: "0.75rem" }}>
                  {step.scenario.agent_steps.map((s, i) => (
                    <div key={i} style={{ display: "flex", gap: "0.75rem", padding: "4px 0", color: VARIANT.colors.success }}>
                      <span style={{ color: VARIANT.colors.accent, fontSize: "0.75rem", minWidth: "100px" }}>[{s.tool}]</span>
                      <span>{s.action}</span>
                      <span style={{ marginLeft: "auto", color: VARIANT.colors.textMuted, fontSize: "0.75rem" }}>{s.time}</span>
                    </div>
                  ))}
                </div>
                <p style={{ marginTop: "0.75rem", fontWeight: "700", color: VARIANT.colors.success }}>
                  Total: {step.scenario.total_time} | {step.scenario.result}
                </p>
              </div>
            </div>
          )}
        </div>
      ))}

      {onboarding.sources.map((s) => <SourceBadge key={s} id={s} />)}
    </div>
  );
}

function AhaScreen() {
  const { aha } = VARIANT;
  return (
    <div style={{ background: VARIANT.colors.bg, color: VARIANT.colors.text, padding: "2rem", borderRadius: "12px", textAlign: "center" }}>
      <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>⚡</div>
      <h2 style={{ fontSize: "2rem", fontWeight: "800", background: `linear-gradient(135deg, ${VARIANT.colors.primary}, ${VARIANT.colors.accent})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
        {aha.title}
      </h2>
      <p style={{ fontSize: "1.1rem", color: VARIANT.colors.textMuted, marginTop: "1rem", maxWidth: "600px", margin: "1rem auto" }}>
        {aha.description}
      </p>
      <div style={{ background: VARIANT.colors.bgLight, padding: "1.5rem", borderRadius: "8px", margin: "1.5rem auto", maxWidth: "400px", border: `2px solid ${VARIANT.colors.success}` }}>
        <div style={{ fontSize: "1.5rem", fontWeight: "800", color: VARIANT.colors.success }}>{aha.wow_metric}</div>
        <div style={{ color: VARIANT.colors.textMuted, marginTop: "0.5rem" }}>KPI: {aha.kpi}</div>
      </div>
      <div style={{ background: VARIANT.colors.bgCard, padding: "1rem", borderRadius: "8px", marginTop: "1.5rem", maxWidth: "500px", margin: "1rem auto" }}>
        <p style={{ fontSize: "0.9rem", color: VARIANT.colors.warning }}>🧪 CustDev Question: {aha.validation_question}</p>
      </div>
      {aha.sources.map((s) => <SourceBadge key={s} id={s} />)}
    </div>
  );
}

function DashboardScreen() {
  const { dashboard } = VARIANT;
  return (
    <div style={{ background: VARIANT.colors.bg, color: VARIANT.colors.text, padding: "2rem", borderRadius: "12px" }}>
      <h2 style={{ fontSize: "1.75rem", marginBottom: "1.5rem" }}>🎛️ {dashboard.name}</h2>

      <div style={{ display: "grid", gridTemplateColumns: "250px 1fr 250px", gap: "1rem" }}>
        {/* Multi-Agent Hub */}
        <div style={{ background: VARIANT.colors.bgLight, padding: "1rem", borderRadius: "8px" }}>
          <h3 style={{ color: VARIANT.colors.accent, fontSize: "0.9rem", marginBottom: "0.75rem" }}>
            🤖 {dashboard.sections.multi_agent_hub.title}
          </h3>
          {dashboard.sections.multi_agent_hub.agents.map((a) => (
            <div key={a.name} style={{ padding: "6px 0", borderBottom: `1px solid ${VARIANT.colors.bgCard}`, fontSize: "0.85rem" }}>
              <div style={{ fontWeight: "600" }}>{a.name}</div>
              <div style={{ color: VARIANT.colors.textMuted, fontSize: "0.75rem" }}>{a.role}</div>
            </div>
          ))}
          <SourceBadge id={dashboard.sections.multi_agent_hub.source} />
        </div>

        {/* Live Conversation */}
        <div style={{ background: VARIANT.colors.bgLight, padding: "1rem", borderRadius: "8px" }}>
          <h3 style={{ color: VARIANT.colors.accent, fontSize: "0.9rem", marginBottom: "0.75rem" }}>
            💬 {dashboard.sections.live_conversation.title}
          </h3>
          <div style={{ background: VARIANT.colors.bg, padding: "0.75rem", borderRadius: "6px" }}>
            <p style={{ color: VARIANT.colors.textMuted }}><em>Customer: "{dashboard.sections.live_conversation.example.customer}"</em></p>
            <p style={{ color: VARIANT.colors.accent, margin: "0.5rem 0", fontSize: "0.85rem" }}>🤖 {dashboard.sections.live_conversation.example.agent_name}:</p>
            {dashboard.sections.live_conversation.example.steps.map((s, i) => (
              <p key={i} style={{ color: VARIANT.colors.success, fontSize: "0.85rem", margin: "2px 0" }}>✓ {s}</p>
            ))}
          </div>
        </div>

        {/* Copilot Panel */}
        <div style={{ background: VARIANT.colors.bgLight, padding: "1rem", borderRadius: "8px" }}>
          <h3 style={{ color: VARIANT.colors.accent, fontSize: "0.9rem", marginBottom: "0.75rem" }}>
            🧠 {dashboard.sections.copilot_panel.title}
          </h3>
          {dashboard.sections.copilot_panel.features.map((f) => (
            <div key={f.name} style={{ padding: "6px 0", borderBottom: `1px solid ${VARIANT.colors.bgCard}`, fontSize: "0.85rem" }}>
              <div><span>{f.icon}</span> <strong>{f.name}</strong></div>
              <div style={{ color: VARIANT.colors.textMuted, fontSize: "0.75rem" }}>{f.description}</div>
              {f.source && <SourceLink id={f.source} />}
            </div>
          ))}
          <SourceBadge id={dashboard.sections.copilot_panel.source} />
        </div>
      </div>

      {/* Analytics Bar */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "0.75rem", marginTop: "1.5rem" }}>
        {dashboard.sections.analytics.metrics.map((m) => (
          <div key={m.label} style={{ background: VARIANT.colors.bgLight, padding: "1rem", borderRadius: "8px", textAlign: "center" }}>
            <div style={{ fontSize: "1.5rem", fontWeight: "800", color: VARIANT.colors.accent }}>{m.value}</div>
            <div style={{ fontSize: "0.75rem", color: VARIANT.colors.textMuted }}>{m.label}</div>
            {m.pct && <div style={{ fontSize: "0.85rem", color: VARIANT.colors.success }}>{m.pct}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}

function PaywallScreen() {
  const { paywall } = VARIANT;
  const plans = Object.values(paywall.plans);
  return (
    <div style={{ background: VARIANT.colors.bg, color: VARIANT.colors.text, padding: "2rem", borderRadius: "12px" }}>
      <h2 style={{ fontSize: "1.75rem", textAlign: "center", marginBottom: "0.5rem" }}>Simple, Transparent Pricing</h2>
      <p style={{ textAlign: "center", color: VARIANT.colors.textMuted, marginBottom: "2rem" }}>Self-hosted is free forever. Cloud scales with you.</p>

      <div style={{ display: "grid", gridTemplateColumns: `repeat(${plans.length}, 1fr)`, gap: "1rem" }}>
        {plans.map((plan) => (
          <div key={plan.name} style={{
            background: VARIANT.colors.bgLight,
            padding: "1.5rem",
            borderRadius: "8px",
            border: plan.name === "Starter" ? `2px solid ${VARIANT.colors.primary}` : `1px solid ${VARIANT.colors.bgCard}`,
            position: "relative",
          }}>
            {plan.name === "Starter" && (
              <div style={{ position: "absolute", top: "-12px", left: "50%", transform: "translateX(-50%)", background: VARIANT.colors.primary, color: "#fff", padding: "2px 12px", borderRadius: "999px", fontSize: "0.75rem" }}>
                MOST POPULAR
              </div>
            )}
            <h3 style={{ color: VARIANT.colors.accent }}>{plan.name}</h3>
            <div style={{ margin: "0.75rem 0" }}>
              <span style={{ fontSize: "2rem", fontWeight: "800" }}>{plan.price}</span>
              <span style={{ color: VARIANT.colors.textMuted }}>{plan.period}</span>
            </div>
            <p style={{ color: VARIANT.colors.textMuted, fontSize: "0.85rem", marginBottom: "1rem" }}>{plan.tagline}</p>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {plan.features.map((f, i) => (
                <li key={i} style={{ padding: "4px 0", fontSize: "0.85rem", color: VARIANT.colors.text }}>
                  ✓ {f}
                </li>
              ))}
            </ul>
            {plan.comparison && (
              <div style={{ marginTop: "1rem", padding: "8px", background: VARIANT.colors.bgCard, borderRadius: "4px", fontSize: "0.75rem", color: VARIANT.colors.warning }}>
                💡 {plan.comparison}
              </div>
            )}
            <button style={{
              width: "100%", marginTop: "1rem", padding: "10px",
              background: plan.name === "Starter" ? VARIANT.colors.primary : "transparent",
              color: plan.name === "Starter" ? "#fff" : VARIANT.colors.primary,
              border: plan.name === "Starter" ? "none" : `1px solid ${VARIANT.colors.primary}`,
              borderRadius: "6px", cursor: "pointer", fontWeight: "600",
            }}>
              {plan.cta}
            </button>
            {plan.sources && (
              <div style={{ marginTop: "0.75rem" }}>
                {plan.sources.map((s) => <SourceLink key={s} id={s} />)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function CommerceScreen() {
  const { commerce } = VARIANT;
  return (
    <div style={{ background: VARIANT.colors.bg, color: VARIANT.colors.text, padding: "2rem", borderRadius: "12px" }}>
      <h2 style={{ fontSize: "1.75rem", marginBottom: "0.5rem" }}>🛒 {commerce.title}</h2>
      <div style={{ background: VARIANT.colors.bgLight, padding: "1.5rem", borderRadius: "8px", marginTop: "1rem" }}>
        <p style={{ color: VARIANT.colors.textMuted }}>Customer: <em>"{commerce.example.customer}"</em></p>
        {commerce.example.agent_steps.map((s, i) => (
          <div key={i} style={{ marginTop: "0.5rem", padding: "8px", background: VARIANT.colors.bg, borderRadius: "6px" }}>
            {s.type === "product_card" && (
              <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                <div style={{ width: "60px", height: "60px", background: VARIANT.colors.primary, borderRadius: "8px", display: "flex", alignItems: "center", justifyContent: "center" }}>🔵</div>
                <div>
                  <div style={{ fontWeight: "600" }}>{s.action.split("—")[0]}</div>
                  <div style={{ color: VARIANT.colors.accent, fontWeight: "800" }}>{s.action.split("—")[1]}</div>
                </div>
              </div>
            )}
            {s.type === "checkout" && (
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <button style={{ padding: "8px 16px", background: VARIANT.colors.bgCard, borderRadius: "6px", border: "none", color: VARIANT.colors.text, cursor: "pointer" }}>🛒 Add to Cart</button>
                <button style={{ padding: "8px 16px", background: VARIANT.colors.primary, borderRadius: "6px", border: "none", color: "#fff", cursor: "pointer" }}>💳 Pay in Chat — Stripe</button>
              </div>
            )}
            {s.type === "confirmation" && (
              <p style={{ color: VARIANT.colors.success, fontWeight: "600" }}>✅ {s.action}</p>
            )}
          </div>
        ))}
      </div>
      <div style={{ marginTop: "1rem" }}>
        {commerce.sources.map((s) => <SourceBadge key={s} id={s} />)}
      </div>
    </div>
  );
}

// ============================================================
// CJM OVERLAY BADGE
// ============================================================
function CJMOverlay({ stage }) {
  const meta = CJM_META[stage];
  if (!meta) return null;
  return (
    <div style={{
      background: "rgba(99, 102, 241, 0.15)",
      border: `1px solid ${VARIANT.colors.primary}`,
      borderRadius: "8px",
      padding: "0.75rem 1rem",
      marginBottom: "1rem",
      fontSize: "0.85rem",
    }}>
      <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <span style={{ background: VARIANT.colors.primary, color: "#fff", padding: "2px 8px", borderRadius: "4px", fontSize: "0.75rem" }}>
          {meta.aarrr}
        </span>
        <span style={{ fontWeight: "600" }}>{meta.stage}</span>
        <span style={{ color: VARIANT.colors.textMuted }}>Metric: {meta.metric}</span>
      </div>
      <p style={{ color: VARIANT.colors.warning, marginTop: "0.5rem" }}>🧪 {meta.question}</p>
    </div>
  );
}

// ============================================================
// SCORING COMPONENT
// ============================================================
function Scoring() {
  const scores = [
    { label: "Time to Aha", value: "12 min", score: 4, max: 5 },
    { label: "Market Size", value: "$52.62B by 2030", score: 5, max: 5 },
    { label: "Build Complexity", value: "High (phased MVP)", score: 3, max: 5 },
    { label: "Differentiation", value: "Unique: agentic + OSS + self-hosted", score: 5, max: 5 },
    { label: "Monetization", value: "$0.49/resolution + seats", score: 4, max: 5 },
    { label: "Defensibility", value: "OSS community + MCP ecosystem", score: 4, max: 5 },
  ];
  const total = scores.reduce((a, s) => a + s.score, 0);
  const totalMax = scores.reduce((a, s) => a + s.max, 0);

  return (
    <div style={{ background: VARIANT.colors.bg, color: VARIANT.colors.text, padding: "2rem", borderRadius: "12px" }}>
      <h2 style={{ fontSize: "1.75rem", marginBottom: "1.5rem" }}>🏆 Scoring: Hybrid B+D</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem" }}>
        {scores.map((s) => (
          <div key={s.label} style={{ background: VARIANT.colors.bgLight, padding: "1rem", borderRadius: "8px" }}>
            <div style={{ fontSize: "0.85rem", color: VARIANT.colors.textMuted }}>{s.label}</div>
            <div style={{ fontSize: "1.25rem", fontWeight: "700", color: VARIANT.colors.accent, margin: "0.25rem 0" }}>
              {"⭐".repeat(s.score)}{"☆".repeat(s.max - s.score)}
            </div>
            <div style={{ fontSize: "0.8rem", color: VARIANT.colors.text }}>{s.value}</div>
          </div>
        ))}
      </div>
      <div style={{ textAlign: "center", marginTop: "1.5rem", fontSize: "2rem", fontWeight: "800", color: VARIANT.colors.success }}>
        Total: {total}/{totalMax}
      </div>
    </div>
  );
}

// ============================================================
// SOURCES PANEL
// ============================================================
function SourcesPanel() {
  return (
    <div style={{ background: VARIANT.colors.bg, color: VARIANT.colors.text, padding: "2rem", borderRadius: "12px" }}>
      <h2 style={{ fontSize: "1.75rem", marginBottom: "1.5rem" }}>📎 All Sources</h2>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.5rem" }}>
        {Object.entries(SOURCES).map(([key, src]) => (
          <a
            key={key}
            href={src.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: "block",
              padding: "8px 12px",
              background: VARIANT.colors.bgLight,
              borderRadius: "6px",
              color: VARIANT.colors.text,
              textDecoration: "none",
              fontSize: "0.8rem",
              borderLeft: `3px solid ${VARIANT.colors.accent}`,
            }}
          >
            <div style={{ color: VARIANT.colors.accent, fontWeight: "600" }}>{src.publisher}</div>
            <div style={{ color: VARIANT.colors.textMuted, marginTop: "2px" }}>{src.fact}</div>
          </a>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// MAIN APP
// ============================================================
const SCREENS = [
  { id: "landing", label: "🏠 Landing", component: LandingScreen },
  { id: "onboarding", label: "🚀 Onboarding", component: OnboardingScreen },
  { id: "aha", label: "⚡ Aha Moment", component: AhaScreen },
  { id: "dashboard", label: "🎛️ Command Center", component: DashboardScreen },
  { id: "paywall", label: "💰 Pricing", component: PaywallScreen },
  { id: "commerce", label: "🛒 Commerce", component: CommerceScreen },
  { id: "scoring", label: "🏆 Scoring", component: Scoring },
  { id: "sources", label: "📎 Sources", component: SourcesPanel },
];

export default function CJMPrototype() {
  const [activeScreen, setActiveScreen] = useState("landing");
  const [showOverlay, setShowOverlay] = useState(true);

  const ActiveComponent = SCREENS.find((s) => s.id === activeScreen)?.component || LandingScreen;

  return (
    <div style={{ fontFamily: "'Inter', -apple-system, sans-serif", maxWidth: "1200px", margin: "0 auto", padding: "1rem" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <div>
          <h1 style={{ fontSize: "1.5rem", color: VARIANT.colors.text, margin: 0 }}>
            {VARIANT.emoji} CJM: {VARIANT.name}
          </h1>
          <p style={{ color: VARIANT.colors.textMuted, fontSize: "0.85rem", margin: 0 }}>
            Hybrid B (Developer-First) + D (Agentic Platform 2026)
          </p>
        </div>
        <button
          onClick={() => setShowOverlay(!showOverlay)}
          style={{
            padding: "6px 14px",
            background: showOverlay ? VARIANT.colors.primary : VARIANT.colors.bgCard,
            color: "#fff",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontSize: "0.85rem",
          }}
        >
          {showOverlay ? "🔍 CJM Overlay ON" : "🔍 CJM Overlay OFF"}
        </button>
      </div>

      {/* Screen Tabs */}
      <div style={{ display: "flex", gap: "0.25rem", marginBottom: "1rem", flexWrap: "wrap" }}>
        {SCREENS.map((screen) => (
          <button
            key={screen.id}
            onClick={() => setActiveScreen(screen.id)}
            style={{
              padding: "8px 16px",
              background: activeScreen === screen.id ? VARIANT.colors.primary : VARIANT.colors.bgLight,
              color: activeScreen === screen.id ? "#fff" : VARIANT.colors.textMuted,
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              fontSize: "0.85rem",
              fontWeight: activeScreen === screen.id ? "600" : "400",
            }}
          >
            {screen.label}
          </button>
        ))}
      </div>

      {/* CJM Overlay */}
      {showOverlay && <CJMOverlay stage={activeScreen} />}

      {/* Active Screen */}
      <ActiveComponent />
    </div>
  );
}
