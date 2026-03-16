"use client";

import { useState } from "react";
import AnalysisView from "@/components/AnalysisView";
import ChatView from "@/components/ChatView";
import { FileText, MessageSquare, Zap } from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"analyze" | "chat">("analyze");

  return (
    <div className="min-h-screen bg-[#F0F4F8]">
      {/* Top Nav */}
      <header className="bg-[#0A1628] text-white shadow-lg">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-[#00C8A0] rounded-lg p-2">
              <Zap className="w-5 h-5 text-[#0A1628]" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">adviZor</h1>
              <p className="text-xs text-[#718096]">AI Campaign Portfolio Advisor</p>
            </div>
          </div>
          <div className="text-xs text-[#718096]">
            Client: <span className="text-[#00C8A0] font-semibold">NovaPulse Energy</span>
          </div>
        </div>
      </header>

      {/* Tab Bar */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex gap-0">
            <button
              onClick={() => setActiveTab("analyze")}
              className={`flex items-center gap-2 px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === "analyze"
                  ? "border-[#00C8A0] text-[#0A1628]"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              <FileText className="w-4 h-4" />
              Auto-Analysis
            </button>
            <button
              onClick={() => setActiveTab("chat")}
              className={`flex items-center gap-2 px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === "chat"
                  ? "border-[#00C8A0] text-[#0A1628]"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              Ask adviZor
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        {activeTab === "analyze" ? <AnalysisView /> : <ChatView />}
      </main>
    </div>
  );
}
