import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import MetricCard from "../components/MetricCard";
import { api } from "../api/client";

interface IRoiMetrics {
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
  daily_trend: { date: string; consultations: number; leads: number }[];
}

const PERIODS = [
  { value: "7d", label: "7 days" },
  { value: "30d", label: "30 days" },
  { value: "90d", label: "90 days" },
];

const QUALIFICATION_COLORS: Record<string, string> = {
  cold: "#94a3b8",
  warm: "#fbbf24",
  hot: "#f97316",
  qualified: "#22c55e",
};

const QUALIFICATION_LABELS: Record<string, string> = {
  cold: "Cold",
  warm: "Warm",
  hot: "Hot",
  qualified: "Qualified",
};

const CHANNEL_LABELS: Record<string, string> = {
  telegram: "Telegram",
  web_widget: "Web Widget",
  crm: "CRM",
};

function formatCurrency(value: number): string {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M ₽`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(0)}K ₽`;
  return `${value.toFixed(0)} ₽`;
}

export default function RoiAnalyticsPage() {
  const [period, setPeriod] = useState("30d");
  const [metrics, setMetrics] = useState<IRoiMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    api
      .getRoiMetrics(period)
      .then(setMetrics)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [period]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">{error}</div>
    );
  }

  if (!metrics) return null;

  const aiVsSaData = [
    { name: "AI-handled", value: metrics.ai_handled, fill: "#3b82f6" },
    { name: "Escalated to SA", value: metrics.escalated_to_sa, fill: "#f97316" },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">ROI Analytics</h2>
          <p className="text-sm text-gray-500 mt-1">
            AI consultant performance and business impact
          </p>
        </div>
        <div className="flex gap-1 bg-gray-100 rounded-lg p-1">
          {PERIODS.map((p) => (
            <button
              key={p.value}
              onClick={() => setPeriod(p.value)}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${
                period === p.value
                  ? "bg-white text-gray-900 shadow-sm"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Key ROI Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="SA Hours Saved"
          value={`${metrics.sa_hours_saved}h`}
          subtitle={formatCurrency(metrics.sa_cost_saved)}
          trend="up"
        />
        <MetricCard
          title="Pipeline Value"
          value={formatCurrency(metrics.pipeline_value)}
          subtitle={`${metrics.qualified_leads} qualified leads`}
          trend={metrics.qualified_leads > 0 ? "up" : "neutral"}
        />
        <MetricCard
          title="Conversion Rate"
          value={`${(metrics.conversion_rate * 100).toFixed(1)}%`}
          subtitle={`${metrics.total_leads} / ${metrics.total_consultations}`}
        />
        <MetricCard
          title="Avg Deal Value"
          value={metrics.avg_deal_value ? formatCurrency(metrics.avg_deal_value) : "N/A"}
        />
      </div>

      {/* Charts row 1: AI vs SA + Lead Funnel */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI vs SA handling */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-4">AI vs SA Handling</h3>
          <div className="flex items-center gap-8">
            <ResponsiveContainer width="50%" height={200}>
              <PieChart>
                <Pie
                  data={aiVsSaData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  dataKey="value"
                >
                  {aiVsSaData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number) => [value, "consultations"]} />
              </PieChart>
            </ResponsiveContainer>
            <div className="space-y-3">
              <div>
                <div className="text-2xl font-bold text-blue-600">{metrics.ai_handled}</div>
                <div className="text-sm text-gray-500">Handled by AI</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-orange-500">{metrics.escalated_to_sa}</div>
                <div className="text-sm text-gray-500">Escalated to SA</div>
              </div>
              <div className="pt-2 border-t">
                <div className="text-sm text-gray-600">
                  AI handles{" "}
                  <span className="font-semibold">
                    {metrics.total_consultations > 0
                      ? ((metrics.ai_handled / metrics.total_consultations) * 100).toFixed(0)
                      : 0}
                    %
                  </span>{" "}
                  of consultations
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Lead qualification breakdown */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-4">Lead Funnel</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart
              data={metrics.lead_breakdown.map((b) => ({
                ...b,
                label: QUALIFICATION_LABELS[b.qualification] || b.qualification,
              }))}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="label" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip
                formatter={(value: number, name: string) => {
                  if (name === "total_value") return [formatCurrency(value), "Value"];
                  return [value, "Leads"];
                }}
              />
              <Bar dataKey="count" name="Leads">
                {metrics.lead_breakdown.map((b, i) => (
                  <Cell key={i} fill={QUALIFICATION_COLORS[b.qualification] || "#94a3b8"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts row 2: Channel stats + Daily trend */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Channel performance */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-4">Channel Performance</h3>
          <div className="space-y-3">
            {metrics.channel_stats.map((ch) => (
              <div key={ch.channel} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">
                    {CHANNEL_LABELS[ch.channel] || ch.channel}
                  </div>
                  <div className="text-xs text-gray-500">
                    {ch.consultations} consultations / {ch.leads} leads
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-semibold text-primary-600">
                    {(ch.conversion_rate * 100).toFixed(1)}%
                  </div>
                  <div className="text-xs text-gray-500">conversion</div>
                </div>
              </div>
            ))}
            {metrics.channel_stats.length === 0 && (
              <div className="text-sm text-gray-400 text-center py-4">No channel data yet</div>
            )}
          </div>
        </div>

        {/* Daily trend */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-4">Daily Trend</h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={metrics.daily_trend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 12 }}
                tickFormatter={(v: string) =>
                  new Date(v).toLocaleDateString("ru-RU", { day: "numeric", month: "short" })
                }
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip
                labelFormatter={(v: string) => new Date(v).toLocaleDateString("ru-RU")}
              />
              <Legend />
              <Line type="monotone" dataKey="consultations" stroke="#3b82f6" strokeWidth={2} name="Consultations" />
              <Line type="monotone" dataKey="leads" stroke="#22c55e" strokeWidth={2} name="Leads" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Cost savings summary */}
      <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-xl border border-blue-100 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Cost Savings Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <div className="text-sm text-gray-600">SA hours replaced by AI</div>
            <div className="text-2xl font-bold text-blue-700">{metrics.sa_hours_saved}h</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Cost saved (SA rate: 5,000 ₽/h)</div>
            <div className="text-2xl font-bold text-green-700">
              {formatCurrency(metrics.sa_cost_saved)}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Pipeline generated</div>
            <div className="text-2xl font-bold text-purple-700">
              {formatCurrency(metrics.pipeline_value)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
