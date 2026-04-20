"use client";

import React from "react";
import { motion } from "framer-motion";
import { 
  ShieldCheck, AlertTriangle, XCircle, Info, 
  ArrowUpRight, ArrowDownRight, CheckCircle2, 
  ExternalLink, FileText, Scale
} from "lucide-react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, Cell, PieChart, Pie 
} from "recharts";
import { PredictionResponse } from "@/lib/api";
import { cn, formatCurrency } from "@/lib/utils";

const ResultsDashboard = ({ data }: { data: PredictionResponse }) => {
  const { lending_decision, risk_analysis, policy_retrieval, foir, dti, proposed_emi } = data;

  const decisionStatus = lending_decision?.recommendation?.toLowerCase() || "manual review";
  const isApproved = decisionStatus === "approve";
  const isReview = decisionStatus === "manual review" || decisionStatus === "review";
  const isReject = decisionStatus === "reject";

  const chartData = [
    { name: "Current FOIR", value: (foir * 100).toFixed(1), limit: 40, color: foir > 0.4 ? "#ef4444" : "#3b82f6" },
    { name: "Current DTI", value: (dti * 100).toFixed(1), limit: 50, color: dti > 0.5 ? "#ef4444" : "#3b82f6" },
  ];

  return (
    <div className="w-full space-y-8 pb-20">
      {/* Header Decision Card */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className={cn(
          "glass p-8 rounded-[2rem] border relative overflow-hidden",
          isApproved ? "border-green-500/30" : isReview ? "border-yellow-500/30" : "border-red-500/30"
        )}
      >
        <div className={cn(
          "absolute -top-4 -right-4 p-8 opacity-[0.03] scale-150 pointer-events-none",
          isApproved ? "text-green-500" : isReview ? "text-yellow-500" : "text-red-500"
        )}>
          {isApproved ? <ShieldCheck className="w-64 h-64" /> : isReview ? <AlertTriangle className="w-64 h-64" /> : <XCircle className="w-64 h-64" />}
        </div>

        <div className="relative z-10 flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-8">
          <div className="flex-1 space-y-4">
            <div className={cn(
              "inline-flex items-center gap-2 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest",
              isApproved ? "bg-green-500/20 text-green-400" : isReview ? "bg-yellow-500/20 text-yellow-400" : "bg-red-500/20 text-red-400"
            )}>
              {isApproved ? <CheckCircle2 className="w-3 h-3" /> : isReject ? <XCircle className="w-3 h-3" /> : <Info className="w-3 h-3" />}
              AI Recommendation
            </div>
            <h2 className="text-3xl md:text-4xl font-black tracking-tight leading-[1.1]">{lending_decision.primary_reason}</h2>
            <p className="text-lg text-muted-foreground leading-relaxed max-w-2xl">{lending_decision.suggested_action}</p>
          </div>
          
          <div className="bg-white/5 p-8 rounded-[1.5rem] border border-white/10 flex flex-col items-center justify-center min-w-[180px] text-center">
            <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1">Risk Score</div>
            <div className="text-5xl font-black text-primary tracking-tighter">
              {risk_analysis.risk_score.toFixed(1)}
              <span className="text-xl font-normal text-muted-foreground/50">/100</span>
            </div>
            <div className={cn(
                "mt-3 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full",
                risk_analysis.risk_level.toLowerCase() === "low" ? "bg-green-500/10 text-green-400" : "bg-primary/10 text-primary"
            )}>
              {risk_analysis.risk_level} Risk
            </div>
          </div>
        </div>
      </motion.div>

      <div className="flex flex-col gap-8 w-full">
        {/* Financial Capacity Analysis */}
        <div className="glass p-8 rounded-[2rem] border border-white/10 w-full">
          <h3 className="text-xl font-bold mb-8 flex items-center gap-2">
            <Scale className="w-5 h-5 text-primary" />
            Financial Capacity Analysis
          </h3>
          <div className="h-[350px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ left: 20, right: 40 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                <XAxis type="number" domain={[0, 100]} hide />
                <YAxis dataKey="name" type="category" stroke="#a1a1aa" fontSize={12} width={100} />
                <Tooltip 
                  cursor={{fill: 'rgba(255,255,255,0.05)'}}
                  contentStyle={{ backgroundColor: '#18181b', border: '1px solid #3f3f46', borderRadius: '12px' }}
                />
                <Bar dataKey="value" radius={[0, 8, 8, 0]} barSize={40}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-4 mt-8 text-center">
            <MetricBox label="Proposed EMI" value={formatCurrency(proposed_emi)} />
            <div className="bg-primary/5 border border-primary/20 p-5 rounded-2xl flex flex-col justify-center">
              <div className="text-[10px] font-bold text-primary uppercase tracking-widest mb-1">Status</div>
              <div className="text-lg font-black text-primary">Live Analysis</div>
            </div>
          </div>
        </div>

        {/* Factors */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">
          {/* Positive Factors */}
          <div className="glass p-8 rounded-[2rem] border border-green-500/10 h-full">
            <h4 className="text-lg font-bold text-green-400 mb-6 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5" />
              Strengths
            </h4>
            <ul className="space-y-4 cursor-default">
              {risk_analysis.positive_factors.map((factor, i) => (
                <li key={i} className="flex gap-3 text-sm text-foreground/80 leading-relaxed transition-colors hover:text-foreground">
                  <div className="mt-1 flex-shrink-0 w-1.5 h-1.5 rounded-full bg-green-500" />
                  {factor}
                </li>
              ))}
            </ul>
          </div>
          {/* Risk Factors */}
          <div className="glass p-8 rounded-[2rem] border border-red-500/10 h-full">
            <h4 className="text-lg font-bold text-red-400 mb-6 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Risk Factors
            </h4>
            <ul className="space-y-4 cursor-default">
              {risk_analysis.top_risk_factors.map((factor, i) => (
                <li key={i} className="flex gap-3 text-sm text-foreground/80 leading-relaxed transition-colors hover:text-foreground">
                  <div className="mt-1 flex-shrink-0 w-1.5 h-1.5 rounded-full bg-red-500" />
                  {factor}
                </li>
              ))}
            </ul>
          </div>
        </div>


      </div>
    </div>
  );
};

const MetricBox = ({ label, value }: { label: string; value: string }) => (
  <div className="bg-white/5 border border-white/10 p-5 rounded-2xl">
    <div className="text-xs font-medium text-muted-foreground mb-1 uppercase tracking-wider">{label}</div>
    <div className="text-xl font-black">{value}</div>
  </div>
);

const PolicyStatus = ({ status }: { status: string }) => {
  const normStatus = status.toLowerCase();
  const isPassed = normStatus === "compliant" || normStatus === "passed";
  const isWarning = normStatus === "borderline" || normStatus === "warning";
  return (
    <div className={cn(
      "px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest",
      isPassed ? "bg-green-500/20 text-green-400" : isWarning ? "bg-yellow-500/20 text-yellow-400" : "bg-red-500/20 text-red-400"
    )}>
      {status}
    </div>
  );
};

export const PolicyAudit = ({ policies }: { policies: any[] }) => (
  <div className="glass p-8 rounded-[2rem] border border-white/10 w-full">
    <h3 className="text-xl font-bold mb-8 flex items-center gap-2">
      <FileText className="w-5 h-5 text-primary" />
      Policy Compliance
    </h3>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {policies.map((policy, i) => (
        <div key={i} className="p-5 rounded-2xl bg-white/5 border border-white/10 space-y-3 cursor-pointer hover:bg-white/10 transition-colors duration-200">
          <div className="flex items-center justify-between gap-2">
            <span className="text-xs font-bold text-primary uppercase tracking-wider truncate">{policy.rule_name}</span>
            <PolicyStatus status={policy.status} />
          </div>
          <p className="text-xs text-muted-foreground leading-relaxed italic line-clamp-6">"{policy.rule_text}"</p>
          {policy.source && (
            <div className="flex items-center gap-1 text-[10px] text-primary/60 font-medium pt-2 text-primary transition-colors">
              <ExternalLink className="w-3 h-3" />
              Source: {policy.source}
            </div>
          )}
        </div>
      ))}
    </div>
  </div>
);

export default ResultsDashboard;
