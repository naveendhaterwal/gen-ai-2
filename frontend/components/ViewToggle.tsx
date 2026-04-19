"use client";

import React from "react";
import { motion } from "framer-motion";
import { LayoutDashboard, ShieldCheck } from "lucide-react";

interface ViewToggleProps {
  activeTab: "dashboard" | "agents";
  onChange: (tab: "dashboard" | "agents") => void;
}

const ViewToggle: React.FC<ViewToggleProps> = ({ activeTab, onChange }) => {
  return (
    <div className="flex justify-center mb-12">
      <div className="bg-white/5 border border-white/10 p-1.5 rounded-2xl flex relative w-full max-w-[400px]">
        {/* Sliding Indicator */}
        <motion.div
          className="absolute top-1.5 bottom-1.5 bg-primary/20 border border-primary/30 rounded-xl"
          initial={false}
          animate={{
            left: activeTab === "dashboard" ? "6px" : "calc(50% + 3px)",
            right: activeTab === "dashboard" ? "calc(50% + 3px)" : "6px",
          }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
        />

        <button
          onClick={() => onChange("dashboard")}
          className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-bold transition-colors relative z-10 ${
            activeTab === "dashboard" ? "text-primary" : "text-muted-foreground hover:text-white"
          }`}
        >
          <LayoutDashboard className="w-4 h-4" />
          Dashboard
        </button>

        <button
          onClick={() => onChange("agents")}
          className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-bold transition-colors relative z-10 ${
            activeTab === "agents" ? "text-primary" : "text-muted-foreground hover:text-white"
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          AI Agents
        </button>
      </div>
    </div>
  );
};

export default ViewToggle;
