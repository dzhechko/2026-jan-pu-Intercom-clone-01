import { useState, useEffect } from "react";
import { api } from "../api/client";
import type { ILead } from "../types";

const QUAL_COLORS: Record<string, string> = {
  cold: "bg-blue-100 text-blue-800",
  warm: "bg-yellow-100 text-yellow-800",
  hot: "bg-orange-100 text-orange-800",
  qualified: "bg-green-100 text-green-800",
};

function formatCurrency(value: number | null): string {
  if (!value) return "-";
  return new Intl.NumberFormat("ru-RU", { style: "currency", currency: "RUB", maximumFractionDigits: 0 }).format(value);
}

export default function LeadsPage() {
  const [leads, setLeads] = useState<ILead[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    api
      .getLeads(page)
      .then((data) => {
        setLeads(data.items);
        setTotal(data.total);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [page]);

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

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Leads</h2>
        <p className="text-sm text-gray-500 mt-1">{total} total leads</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Contact</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Company</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Qualification</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Intent</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Est. Value</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Created</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {leads.map((lead) => (
              <tr key={lead.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4">
                  <div className="text-sm font-medium text-gray-900">
                    {lead.contact?.name || "Unknown"}
                  </div>
                  {lead.contact?.email && (
                    <div className="text-xs text-gray-500">{lead.contact.email}</div>
                  )}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  {lead.contact?.company || "-"}
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium ${QUAL_COLORS[lead.qualification] || "bg-gray-100 text-gray-800"}`}>
                    {lead.qualification}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  {lead.intent?.replace(/_/g, " ") || "-"}
                </td>
                <td className="px-6 py-4 text-sm font-medium text-gray-900">
                  {formatCurrency(lead.estimated_deal_value)}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {new Date(lead.created_at).toLocaleDateString("ru-RU", {
                    day: "numeric",
                    month: "short",
                  })}
                </td>
              </tr>
            ))}
            {leads.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                  No leads yet
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {Math.ceil(total / 20) > 1 && (
        <div className="flex items-center justify-center gap-2">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>
          <span className="text-sm text-gray-500">Page {page}</span>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={leads.length < 20}
            className="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
