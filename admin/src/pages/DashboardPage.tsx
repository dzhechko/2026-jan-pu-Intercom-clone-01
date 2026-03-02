import { useState } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import MetricCard from "../components/MetricCard";
import { useDashboard } from "../hooks/useDashboard";

const PERIODS = [
  { value: "today", label: "Today" },
  { value: "7d", label: "7 days" },
  { value: "30d", label: "30 days" },
];

export default function DashboardPage() {
  const [period, setPeriod] = useState("7d");
  const { metrics, loading, error } = useDashboard(period);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
        {error}
      </div>
    );
  }

  if (!metrics) return null;

  const avgResponseSec = metrics.avg_response_time_ms
    ? (metrics.avg_response_time_ms / 1000).toFixed(1) + "s"
    : "N/A";

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
          <p className="text-sm text-gray-500 mt-1">Consultation metrics overview</p>
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

      {/* Metric cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Consultations"
          value={metrics.total_consultations}
        />
        <MetricCard
          title="Leads Generated"
          value={metrics.leads_generated}
          subtitle={`${(metrics.conversion_rate * 100).toFixed(1)}% conversion`}
          trend={metrics.conversion_rate > 0.2 ? "up" : "neutral"}
        />
        <MetricCard
          title="Avg Response Time"
          value={avgResponseSec}
        />
        <MetricCard
          title="Escalation Rate"
          value={`${(metrics.escalation_rate * 100).toFixed(1)}%`}
          trend={metrics.escalation_rate < 0.15 ? "up" : "down"}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trend chart */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-4">Daily Trend</h3>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={metrics.daily_trend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 12 }}
                tickFormatter={(v: string) => new Date(v).toLocaleDateString("ru-RU", { day: "numeric", month: "short" })}
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip
                labelFormatter={(v: string) => new Date(v).toLocaleDateString("ru-RU")}
              />
              <Line type="monotone" dataKey="consultations" stroke="#3b82f6" strokeWidth={2} name="Consultations" />
              <Line type="monotone" dataKey="leads" stroke="#10b981" strokeWidth={2} name="Leads" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Top intents chart */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-4">Top Intents</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={metrics.top_intents} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" tick={{ fontSize: 12 }} />
              <YAxis
                dataKey="intent"
                type="category"
                width={120}
                tick={{ fontSize: 12 }}
                tickFormatter={(v: string) => v.replace(/_/g, " ")}
              />
              <Tooltip formatter={(value: number) => [value, "Count"]} />
              <Bar dataKey="count" fill="#3b82f6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
