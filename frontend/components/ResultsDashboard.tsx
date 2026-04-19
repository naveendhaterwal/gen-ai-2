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
    <div className="max-w-6xl mx-auto w-full space-y-8 pb-20">
      {/* Header Decision Card */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className={cn(
          "glass p-10 rounded-[2.5rem] border-2 relative overflow-hidden",
          isApproved ? "border-green-500/30" : isReview ? "border-yellow-500/30" : "border-red-500/30"
        )}
      >
        <div className={cn(
          "absolute top-0 right-0 p-12 opacity-[0.05]",
          isApproved ? "text-green-500" : isReview ? "text-yellow-500" : "text-red-500"
        )}>
          {isApproved ? <ShieldCheck className="w-32 h-32" /> : isReview ? <AlertTriangle className="w-32 h-32" /> : <XCircle className="w-32 h-32" />}
        </div>

        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
          <div className="space-y-4">
            <div className={cn(
              "inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-widest",
              isApproved ? "bg-green-500/20 text-green-400" : isReview ? "bg-yellow-500/20 text-yellow-400" : "bg-red-500/20 text-red-400"
            )}>
              {isApproved ? <CheckCircle2 className="w-4 h-4" /> : isReject ? <XCircle className="w-4 h-4" /> : <Info className="w-4 h-4" />}
              AI Recommendation: {lending_decision.recommendation}
            </div>
            <h2 className="text-4xl md:text-5xl font-black">{lending_decision.primary_reason}</h2>
            <p className="text-xl text-muted-foreground">{lending_decision.suggested_action}</p>
          </div>
          
          <div className="bg-white/5 p-6 rounded-3xl border border-white/10 min-w-[200px]">
            <div className="text-sm font-medium text-muted-foreground mb-1">Risk Score</div>
            <div className="text-5xl font-black text-primary">
              {risk_analysis.risk_score.toFixed(1)}
              <span className="text-xl font-normal text-muted-foreground">/100</span>
            </div>
            <div className="mt-2 text-sm font-semibold capitalize inline-block px-3 py-1 bg-primary/10 rounded-lg text-primary">
              {risk_analysis.risk_level} Risk
            </div>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Metrics & Factors */}
        <div className="lg:col-span-2 space-y-8">
          {/* Key Metrics Chart */}
          <div className="glass p-8 rounded-[2rem] border border-white/10">
            <h3 className="text-xl font-bold mb-8 flex items-center gap-2">
              <Scale className="w-5 h-5 text-primary" />
              Financial Capacity Analysis
            </h3>
            <div className="h-[250px] w-full mt-4">
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

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Positive Factors */}
            <div className="glass p-8 rounded-[2rem] border border-green-500/10">
              <h4 className="text-lg font-bold text-green-400 mb-6 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5" />
                Strengths
              </h4>
              <ul className="space-y-4">
                {risk_analysis.positive_factors.map((factor, i) => (
                  <li key={i} className="flex gap-3 text-sm text-foreground/80 leading-relaxed">
                    <div className="mt-1 flex-shrink-0 w-1.5 h-1.5 rounded-full bg-green-500" />
                    {factor}
                  </li>
                ))}
              </ul>
            </div>
            {/* Risk Factors */}
            <div className="glass p-8 rounded-[2rem] border border-red-500/10">
              <h4 className="text-lg font-bold text-red-400 mb-6 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                Risk Factors
              </h4>
              <ul className="space-y-4">
                {risk_analysis.top_risk_factors.map((factor, i) => (
                  <li key={i} className="flex gap-3 text-sm text-foreground/80 leading-relaxed">
                    <div className="mt-1 flex-shrink-0 w-1.5 h-1.5 rounded-full bg-red-500" />
                    {factor}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Right Column: Policy Audit */}
        <div className="space-y-8">
          <div className="glass p-8 rounded-[2rem] border border-white/10 h-full">
            <h3 className="text-xl font-bold mb-8 flex items-center gap-2">
              <FileText className="w-5 h-5 text-primary" />
              Policy Compliance
            </h3>
            <div className="space-y-6">
              {policy_retrieval.policies_matched.map((policy, i) => (
                <div key={i} className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-primary uppercase tracking-wider">{policy.rule_name}</span>
                    <PolicyStatus status={policy.status} />
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed italic">"{policy.rule_text}"</p>
                  {policy.source && (
                    <div className="flex items-center gap-1 text-[10px] text-primary/60 font-medium">
                      <ExternalLink className="w-3 h-3" />
                      Source: {policy.source}
                    </div>
                  )}
                </div>
              ))}
            </div>
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

export default ResultsDashboard;
