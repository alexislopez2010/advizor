"use client";

import { useState, useEffect } from "react";
import { Download, RefreshCw, CheckCircle, AlertCircle, TrendingUp, DollarSign, Target } from "lucide-react";

const API = "http://localhost:8000";

interface Service {
  id: string;
  name: string;
  tagline: string;
  description: string;
  monthly_cost_usd: number;
  tiers: string[];
  avg_roi_narrative: string;
  capabilities: string[];
}

interface Recommendation {
  service_id: string;
  service_name: string;
  priority: "High" | "Medium" | "Low";
  goals_addressed: string[];
  reasoning: string;
  expected_value: string;
  recommended_tier: string;
  time_to_impact: string;
}

interface Analysis {
  client: {
    name: string;
    industry: string;
    description: string;
    annual_ad_budget_usd: number;
    current_spend_on_services_monthly: number;
    campaign_goals_2027: string[];
    current_challenges: string[];
  };
  current_subscriptions: Service[];
  gap_services: Service[];
  recommendations: Recommendation[];
  executive_summary: string;
  total_additional_investment: number;
}

const PRIORITY_STYLES = {
  High: "bg-red-100 text-red-700 border border-red-200",
  Medium: "bg-amber-100 text-amber-700 border border-amber-200",
  Low: "bg-green-100 text-green-700 border border-green-200",
};

export default function AnalysisView() {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [error, setError] = useState("");

  const runAnalysis = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/api/analyze`);
      if (!res.ok) throw new Error("Analysis failed");
      const data = await res.json();
      setAnalysis(data);
    } catch (e) {
      setError("Could not connect to adviZor API. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async () => {
    setPdfLoading(true);
    try {
      const res = await fetch(`${API}/api/report/pdf`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "adviZor-NovaPulse-Brief.pdf";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("PDF download failed.");
    } finally {
      setPdfLoading(false);
    }
  };

  useEffect(() => { runAnalysis(); }, []);

  if (loading) return (
    <div className="flex flex-col items-center justify-center py-24 gap-4">
      <div className="w-12 h-12 border-4 border-[#00C8A0] border-t-transparent rounded-full animate-spin" />
      <p className="text-gray-500 text-sm">Running portfolio analysis…</p>
    </div>
  );

  if (error) return (
    <div className="bg-red-50 border border-red-200 rounded-xl p-6 flex items-start gap-3">
      <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
      <div>
        <p className="font-medium text-red-700">Analysis Error</p>
        <p className="text-sm text-red-600 mt-1">{error}</p>
        <button onClick={runAnalysis} className="mt-3 text-sm text-red-600 underline">Try again</button>
      </div>
    </div>
  );

  if (!analysis) return null;

  const currentMonthly = analysis.current_subscriptions.reduce((s, v) => s + v.monthly_cost_usd, 0);
  const newMonthly = currentMonthly + analysis.total_additional_investment;
  const stackPct = ((newMonthly * 12) / analysis.client.annual_ad_budget_usd * 100).toFixed(1);

  return (
    <div className="space-y-6">
      {/* Action Bar */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-[#0A1628]">Portfolio Analysis</h2>
          <p className="text-sm text-gray-500">2027 Campaign Gap Report · {analysis.client.name}</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={runAnalysis}
            className="flex items-center gap-2 px-4 py-2 text-sm border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors"
          >
            <RefreshCw className="w-4 h-4" /> Re-run
          </button>
          <button
            onClick={downloadPDF}
            disabled={pdfLoading}
            className="flex items-center gap-2 px-4 py-2 text-sm bg-[#0A1628] text-white rounded-lg hover:bg-[#1a2d4a] transition-colors disabled:opacity-60"
          >
            <Download className="w-4 h-4" />
            {pdfLoading ? "Generating…" : "Download PDF Brief"}
          </button>
        </div>
      </div>

      {/* Executive Summary */}
      <div className="bg-[#0A1628] rounded-xl p-6 text-white">
        <p className="text-xs font-bold text-[#00C8A0] uppercase tracking-widest mb-2">Executive Summary</p>
        <p className="text-sm leading-relaxed text-gray-200">{analysis.executive_summary}</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <DollarSign className="w-4 h-4 text-[#00C8A0]" />
            <span className="text-xs font-semibold text-gray-500 uppercase">Annual Budget</span>
          </div>
          <p className="text-2xl font-bold text-[#0A1628]">${(analysis.client.annual_ad_budget_usd / 1e6).toFixed(1)}M</p>
        </div>
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-[#00C8A0]" />
            <span className="text-xs font-semibold text-gray-500 uppercase">Recommended Stack</span>
          </div>
          <p className="text-2xl font-bold text-[#0A1628]">${newMonthly.toLocaleString()}<span className="text-sm text-gray-400">/mo</span></p>
          <p className="text-xs text-gray-400 mt-1">{stackPct}% of budget (industry avg 8–12%)</p>
        </div>
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-4 h-4 text-[#00C8A0]" />
            <span className="text-xs font-semibold text-gray-500 uppercase">Goals Covered</span>
          </div>
          <p className="text-2xl font-bold text-[#0A1628]">{analysis.client.campaign_goals_2027.length}</p>
          <p className="text-xs text-gray-400 mt-1">2027 campaign objectives</p>
        </div>
      </div>

      {/* Two-column layout */}
      <div className="grid grid-cols-5 gap-6">
        {/* Client Profile */}
        <div className="col-span-2 space-y-4">
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <h3 className="font-bold text-[#0A1628] text-sm mb-3">Client Profile</h3>
            <p className="text-xs text-gray-600 leading-relaxed">{analysis.client.description}</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <h3 className="font-bold text-[#0A1628] text-sm mb-3">2027 Goals</h3>
            <ul className="space-y-2">
              {analysis.client.campaign_goals_2027.map((g, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-600">
                  <span className="w-4 h-4 bg-[#E6FAF6] text-[#00C8A0] rounded-full flex items-center justify-center text-[10px] font-bold flex-shrink-0 mt-0.5">{i + 1}</span>
                  {g}
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <h3 className="font-bold text-[#0A1628] text-sm mb-3">Current Subscriptions</h3>
            {analysis.current_subscriptions.map(svc => (
              <div key={svc.id} className="border border-[#00C8A0] rounded-lg p-3 bg-[#E6FAF6]">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-[#0A1628] text-sm">{svc.name}</span>
                  <CheckCircle className="w-4 h-4 text-[#00C8A0]" />
                </div>
                <p className="text-xs text-gray-500 mt-1">{svc.tagline}</p>
                <p className="text-xs font-semibold text-[#00C8A0] mt-1">${svc.monthly_cost_usd.toLocaleString()}/mo</p>
              </div>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="col-span-3 space-y-4">
          <h3 className="font-bold text-[#0A1628] text-sm">Recommended Additions</h3>
          {analysis.recommendations.map((rec) => (
            <div key={rec.service_id} className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
              <div className="bg-[#0A1628] px-5 py-3 flex items-center justify-between">
                <span className="font-bold text-white text-sm">{rec.service_name}</span>
                <span className={`text-xs font-bold px-3 py-1 rounded-full ${PRIORITY_STYLES[rec.priority]}`}>
                  {rec.priority} Priority
                </span>
              </div>
              <div className="p-5 space-y-4">
                <div>
                  <p className="text-xs font-bold text-gray-400 uppercase tracking-wide mb-1">Goals Addressed</p>
                  <div className="flex flex-wrap gap-1">
                    {rec.goals_addressed.map((g, i) => (
                      <span key={i} className="text-xs bg-[#E6FAF6] text-[#0A7A60] px-2 py-1 rounded-md">{g}</span>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-xs font-bold text-gray-400 uppercase tracking-wide mb-1">Why This Tool</p>
                  <p className="text-xs text-gray-600 leading-relaxed">{rec.reasoning}</p>
                </div>
                <div className="bg-[#F0F4F8] rounded-lg p-3">
                  <p className="text-xs font-bold text-[#0A1628] mb-1">📈 Expected Impact</p>
                  <p className="text-xs text-gray-600 leading-relaxed">{rec.expected_value}</p>
                </div>
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <p className="font-bold text-gray-400 uppercase tracking-wide mb-1">Recommended Tier</p>
                    <p className="text-[#0A1628] font-semibold">{rec.recommended_tier}</p>
                  </div>
                  <div>
                    <p className="font-bold text-gray-400 uppercase tracking-wide mb-1">Time to Impact</p>
                    <p className="text-[#0A1628]">{rec.time_to_impact}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
