import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";
import Layout from "./components/Layout";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import ConversationsPage from "./pages/ConversationsPage";
import LeadsPage from "./pages/LeadsPage";
import RoiAnalyticsPage from "./pages/RoiAnalyticsPage";

export default function App() {
  const { isAuthenticated, login, logout, loading, error } = useAuth();

  if (!isAuthenticated) {
    return <LoginPage onLogin={login} error={error} loading={loading} />;
  }

  return (
    <Layout onLogout={logout}>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/conversations" element={<ConversationsPage />} />
        <Route path="/leads" element={<LeadsPage />} />
        <Route path="/roi" element={<RoiAnalyticsPage />} />
        <Route path="/login" element={<Navigate to="/" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
