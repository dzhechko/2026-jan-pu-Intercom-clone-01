import { useState, useEffect } from "react";
import { api } from "../api/client";
import type { IConversation } from "../types";

const STATUS_COLORS: Record<string, string> = {
  active: "bg-green-100 text-green-800",
  escalated: "bg-yellow-100 text-yellow-800",
  completed: "bg-gray-100 text-gray-800",
  timeout: "bg-red-100 text-red-800",
};

const CHANNEL_LABELS: Record<string, string> = {
  telegram: "Telegram",
  web_widget: "Web Widget",
  crm: "CRM",
};

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<IConversation[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    api
      .getConversations(page)
      .then((data) => {
        setConversations(data.items);
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

  const totalPages = Math.ceil(total / 20);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Conversations</h2>
        <p className="text-sm text-gray-500 mt-1">{total} total conversations</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Channel</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Intent</th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Created</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {conversations.map((conv) => (
              <tr key={conv.id} className="hover:bg-gray-50 transition-colors cursor-pointer">
                <td className="px-6 py-4 text-sm font-mono text-gray-600">
                  {conv.id.slice(0, 8)}...
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  {CHANNEL_LABELS[conv.channel] || conv.channel}
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium ${STATUS_COLORS[conv.status] || "bg-gray-100 text-gray-800"}`}>
                    {conv.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  {(conv.context as Record<string, string>)?.detected_intent?.replace(/_/g, " ") || "-"}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {new Date(conv.created_at).toLocaleDateString("ru-RU", {
                    day: "numeric",
                    month: "short",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </td>
              </tr>
            ))}
            {conversations.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                  No conversations yet
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-500">
            Page {page} of {totalPages}
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
