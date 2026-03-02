export interface IMetrics {
  total_consultations: number;
  leads_generated: number;
  avg_response_time_ms: number | null;
  escalation_rate: number;
  satisfaction_score: number | null;
  conversion_rate: number;
  top_intents: IIntentCount[];
  daily_trend: IDailyTrend[];
}

export interface IIntentCount {
  intent: string;
  count: number;
  percentage: number;
}

export interface IDailyTrend {
  date: string;
  consultations: number;
  leads: number;
}

export interface IConversation {
  id: string;
  status: string;
  channel: string;
  channel_user_id: string | null;
  context: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface IMessage {
  id: string;
  role: string;
  agent_type: string | null;
  content: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface ILead {
  id: string;
  conversation_id: string;
  contact: {
    name?: string;
    company?: string;
    email?: string;
    phone?: string;
  };
  qualification: string;
  intent: string | null;
  estimated_deal_value: number | null;
  created_at: string;
}

export interface IUser {
  tenant_id: string;
  role: string;
  email: string;
}

export interface IRoiMetrics {
  total_consultations: number;
  total_leads: number;
  qualified_leads: number;
  pipeline_value: number;
  avg_deal_value: number | null;
  conversion_rate: number;
  ai_handled: number;
  escalated_to_sa: number;
  sa_hours_saved: number;
  sa_cost_saved: number;
  lead_breakdown: { qualification: string; count: number; total_value: number }[];
  channel_stats: { channel: string; consultations: number; leads: number; conversion_rate: number }[];
  daily_trend: IDailyTrend[];
}
