"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User } from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const STARTERS = [
  "What services should NovaPulse add for 2027?",
  "How much would the full recommended stack cost?",
  "Why does NovaPulse need CTV advertising?",
  "What's the projected CPA improvement?",
  "How does AmplifyAI help with creative personalization?",
];

export default function ChatView() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi — I'm adviZor, your AI campaign portfolio advisor. I've analyzed NovaPulse Energy's 2027 goals and current subscriptions. Ask me anything about their portfolio gaps, recommended tools, or projected ROI.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (text?: string) => {
    const msg = text || input.trim();
    if (!msg || loading) return;
    setInput("");

    const userMsg: Message = { role: "user", content: msg };
    setMessages((m) => [...m, userMsg]);
    setLoading(true);

    try {
      const history = messages.slice(1); // exclude welcome
      const res = await fetch(`${API}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg, history }),
      });
      const data = await res.json();
      setMessages((m) => [...m, { role: "assistant", content: data.reply }]);
    } catch {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: "Sorry, I couldn't reach the API. Make sure the backend is running." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const formatContent = (content: string) => {
    // Basic markdown-like formatting
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n\n/g, '<br/><br/>')
      .replace(/\n/g, '<br/>');
  };

  return (
    <div className="flex flex-col h-[calc(100vh-180px)] max-h-[800px]">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                msg.role === "assistant" ? "bg-[#0A1628]" : "bg-[#00C8A0]"
              }`}
            >
              {msg.role === "assistant" ? (
                <Bot className="w-4 h-4 text-white" />
              ) : (
                <User className="w-4 h-4 text-white" />
              )}
            </div>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                msg.role === "assistant"
                  ? "bg-white border border-gray-100 shadow-sm text-gray-700"
                  : "bg-[#0A1628] text-white"
              }`}
              dangerouslySetInnerHTML={{ __html: formatContent(msg.content) }}
            />
          </div>
        ))}
        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-[#0A1628] flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-white border border-gray-100 shadow-sm rounded-2xl px-4 py-3">
              <div className="flex gap-1 items-center h-5">
                <span className="w-2 h-2 bg-[#00C8A0] rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-[#00C8A0] rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-[#00C8A0] rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Starter prompts */}
      {messages.length <= 1 && (
        <div className="pb-4">
          <p className="text-xs text-gray-400 mb-2 font-medium uppercase tracking-wide">Try asking:</p>
          <div className="flex flex-wrap gap-2">
            {STARTERS.map((s, i) => (
              <button
                key={i}
                onClick={() => send(s)}
                className="text-xs bg-white border border-gray-200 rounded-full px-3 py-1.5 text-gray-600 hover:border-[#00C8A0] hover:text-[#0A1628] transition-colors"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="border-t border-gray-200 pt-4">
        <div className="flex gap-3 bg-white border border-gray-200 rounded-xl p-2 shadow-sm focus-within:border-[#00C8A0] transition-colors">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder="Ask about NovaPulse's campaign portfolio…"
            className="flex-1 text-sm px-3 py-2 outline-none bg-transparent text-gray-700 placeholder-gray-400"
          />
          <button
            onClick={() => send()}
            disabled={!input.trim() || loading}
            className="bg-[#0A1628] text-white px-4 py-2 rounded-lg text-sm font-medium disabled:opacity-40 hover:bg-[#1a2d4a] transition-colors flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
