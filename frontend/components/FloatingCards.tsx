"use client";

import React from "react";
import { motion } from "framer-motion";
import { AlertTriangle, ShieldCheck, Activity, Scale } from "lucide-react";
import { cn } from "@/lib/utils";

export const FloatingRiskCard = ({ isHighRisk }: { isHighRisk?: boolean }) => (
  <motion.div
    initial={{ x: -20, opacity: 0 }}
    animate={{ x: 0, opacity: 1 }}
    transition={{ delay: 1, duration: 0.8 }}
    className="absolute -left-12 top-1/4 z-20 hidden xl:block"
  >
    <div className={cn(
      "glass p-4 rounded-2xl border-l-4 shadow-2xl animate-bounce-slow",
      isHighRisk ? "border-red-500" : "border-blue-500"
    )}>
      <div className="flex items-center gap-3 mb-2">
        <div className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center",
          isHighRisk ? "bg-red-500/20 text-red-500" : "bg-blue-500/20 text-blue-500"
        )}>
          {isHighRisk ? <AlertTriangle className="w-5 h-5" /> : <Activity className="w-5 h-5" />}
        </div>
        <span className="text-sm font-bold tracking-tight">
          {isHighRisk ? "Risk Detected" : "Stable Metrics"}
        </span>
      </div>
      <p className="text-[10px] text-muted-foreground font-medium uppercase tracking-wider">
        {isHighRisk ? "FOIR Threshold Exceeded (>40%)" : "Debt-to-Income: Healthy Balance"}
      </p>
    </div>
  </motion.div>
);

export const FloatingAnalysisCard = ({ isCompliant }: { isCompliant?: boolean }) => (
  <motion.div
    initial={{ x: 20, opacity: 0 }}
    animate={{ x: 0, opacity: 1 }}
    transition={{ delay: 1.2, duration: 0.8 }}
    className="absolute -right-12 bottom-1/4 z-20 hidden xl:block"
  >
    <div className={cn(
      "glass p-4 rounded-2xl border-l-4 shadow-2xl",
      isCompliant ? "border-green-500" : "border-yellow-500"
    )}>
      <div className="flex items-center gap-3 mb-2">
        <div className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center",
          isCompliant ? "bg-green-500/20 text-green-500" : "bg-yellow-500/20 text-yellow-500"
        )}>
          <ShieldCheck className="w-5 h-5" />
        </div>
        <span className="text-sm font-bold tracking-tight">
          {isCompliant ? "Policy Audit" : "Manual Review"}
        </span>
      </div>
      <div className={cn(
        "px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest inline-block",
        isCompliant ? "bg-green-500/20 text-green-400" : "bg-yellow-500/20 text-yellow-400"
      )}>
        {isCompliant ? "100% RBI COMPLIANT" : "OFF-POLICY DETECTED"}
      </div>
    </div>
  </motion.div>
);
