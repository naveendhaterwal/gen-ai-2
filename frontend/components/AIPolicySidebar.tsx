"use client";

import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Bot, ExternalLink, SendHorizonal, ShieldCheck, AlertTriangle } from "lucide-react";
import { PredictionResponse, chatWithReport } from "@/lib/api";
import { cn } from "@/lib/utils";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

interface AIPolicySidebarProps {
  data: PredictionResponse;
}

const AIPolicySidebar = ({ data }: AIPolicySidebarProps) => {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [chat, setChat] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Ask me anything about this credit decision, policy compliance, FOIR/DTI impact, or next underwriting action.",
    },
  ]);

  const policies = data.policy_retrieval?.policies_matched || [];

  const starterPrompts = useMemo(
    () => [
      "Why is this applicant risky?",
      "Explain policy violations in simple words",
      "What can improve approval chance?",
    ],
    []
  );

  const askAssistant = async (message: string) => {
    const text = message.trim();
    if (!text || isLoading) {
      return;
    }

    setChat((prev) => [...prev, { role: "user", content: text }]);
    setQuery("");
    setIsLoading(true);

    try {
      const response = await chatWithReport({
        request_id: data.request_id,
        message: text,
      });

      const sourceLabel = response.model_source === "groq" ? "Groq" : "Fallback";
      setChat((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `${response.answer}\n\nSource: ${sourceLabel}`,
        },
      ]);
    } catch (error: any) {
      setChat((prev) => [
        ...prev,
        {
          role: "assistant",
          content: error?.message || "Unable to get AI response right now.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const statusClass = (status: string) => {
    const normalized = status.toLowerCase();
    if (normalized === "compliant" || normalized === "passed") return "bg-green-500/20 text-green-400";
    if (normalized === "borderline" || normalized === "warning") return "bg-yellow-500/20 text-yellow-300";
    return "bg-red-500/20 text-red-400";
  };

  return (
    <aside className="glass border border-white/10 rounded-[2rem] h-full lg:sticky lg:top-6 overflow-hidden">
      <div className="p-6 border-b border-white/10 bg-white/[0.02]">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <Bot className="w-5 h-5 text-primary" />
          AI Response Sidebar
        </h3>
        <p className="text-xs text-muted-foreground mt-1">Chat with Groq using the generated report and policy chunks.</p>
      </div>

      <div className="p-4 border-b border-white/10">
        <div className="text-[11px] uppercase tracking-wider font-bold text-muted-foreground mb-2">Quick Ask</div>
        <div className="flex flex-wrap gap-2">
          {starterPrompts.map((prompt) => (
            <button
              key={prompt}
              onClick={() => askAssistant(prompt)}
              className="text-xs px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 transition-colors"
              disabled={isLoading}
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-rows-[minmax(200px,1fr)_auto] lg:h-[72vh]">
        <div className="overflow-y-auto p-4 space-y-4">
          <section className="space-y-3">
            <div className="text-[11px] uppercase tracking-wider font-bold text-muted-foreground">Policy Chunks</div>
            <div className="space-y-3">
              {policies.map((policy, index) => (
                <div key={`${policy.rule_name}-${index}`} className="rounded-xl bg-white/5 border border-white/10 p-3">
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-[10px] font-black text-primary uppercase tracking-widest truncate">
                      {policy.rule_name || "Lending Policy Chunk"}
                    </span>
                    <span className={cn("text-[10px] font-black uppercase px-2 py-0.5 rounded-md shrink-0", statusClass(policy.status))}>
                      {policy.status}
                    </span>
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed break-words max-h-24 overflow-y-auto pr-1">
                    {policy.rule_text}
                  </p>
                  {policy.source && (
                    <div className="mt-2 text-[10px] text-primary/70 inline-flex items-center gap-1">
                      <ExternalLink className="w-3 h-3" />
                      {policy.source}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>

          <section className="space-y-3 pt-2">
            <div className="text-[11px] uppercase tracking-wider font-bold text-muted-foreground">AI Conversation</div>
            {chat.map((message, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className={cn(
                  "rounded-xl p-3 text-xs leading-relaxed whitespace-pre-wrap",
                  message.role === "user"
                    ? "bg-primary/15 border border-primary/30 ml-6"
                    : "bg-white/5 border border-white/10 mr-6"
                )}
              >
                <div className="font-bold mb-1 inline-flex items-center gap-1">
                  {message.role === "assistant" ? <ShieldCheck className="w-3.5 h-3.5" /> : <AlertTriangle className="w-3.5 h-3.5" />}
                  {message.role === "assistant" ? "AI" : "You"}
                </div>
                {message.content}
              </motion.div>
            ))}
            {isLoading && (
              <div className="text-xs text-primary animate-pulse">Thinking with Groq...</div>
            )}
          </section>
        </div>

        <form
          className="border-t border-white/10 p-3"
          onSubmit={(e) => {
            e.preventDefault();
            askAssistant(query);
          }}
        >
          <div className="flex items-center gap-2">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about this AI response..."
              className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-sm outline-none focus:border-primary/50"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="shrink-0 rounded-xl px-3 py-2 bg-primary text-primary-foreground disabled:opacity-50"
            >
              <SendHorizonal className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </aside>
  );
};

export default AIPolicySidebar;
