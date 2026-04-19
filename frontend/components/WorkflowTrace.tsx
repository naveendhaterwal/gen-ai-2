"use client";

import React from "react";
import { motion } from "framer-motion";
import { PredictionResponse, WorkflowTraceStep } from "@/lib/api";
import { Activity, Database, Brain, AlertTriangle, CheckCircle2, Clock3 } from "lucide-react";

interface WorkflowTraceProps {
  data: PredictionResponse;
}

function safeStringify(value: unknown): string {
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

const StepIcon: React.FC<{ step: string }> = ({ step }) => {
  const lower = step.toLowerCase();

  if (lower.includes("ml")) {
    return <Activity className="w-4 h-4 text-primary" />;
  }
  if (lower.includes("risk") || lower.includes("decision")) {
    return <Brain className="w-4 h-4 text-cyan-400" />;
  }
  if (lower.includes("policy")) {
    return <Database className="w-4 h-4 text-amber-400" />;
  }

  return <Clock3 className="w-4 h-4 text-muted-foreground" />;
};

const WorkflowTrace: React.FC<WorkflowTraceProps> = ({ data }) => {
  const trace = data.workflow_trace || [];
  const completedSteps = trace.filter((step) => step.status === "completed").length;
  const failedSteps = trace.filter((step) => step.status === "failed").length;
  const totalDurationMs = trace.reduce((sum, step) => sum + (step.duration_ms || 0), 0);

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="glass rounded-[2rem] border border-white/10 p-8">
        <h2 className="text-2xl font-black mb-4">Backend Workflow Trace</h2>
        <p className="text-sm text-muted-foreground leading-relaxed">
          This view shows real backend execution details for this request: step-by-step inputs, model/source,
          outputs, and score computation details.
        </p>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="rounded-xl bg-white/5 border border-white/10 p-4">
            <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold">Request ID</div>
            <div className="text-xs font-mono mt-1 text-primary/80">{data.request_id}</div>
          </div>
          <div className="rounded-xl bg-white/5 border border-white/10 p-4">
            <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold">Workflow Steps</div>
            <div className="text-xl font-black mt-1">{trace.length}</div>
          </div>
          <div className="rounded-xl bg-white/5 border border-white/10 p-4">
            <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold">Risk Score</div>
            <div className="text-xl font-black mt-1">{data.risk_analysis.risk_score.toFixed(2)} / 100</div>
          </div>
        </div>

        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="rounded-xl bg-green-500/10 border border-green-500/20 p-4">
            <div className="text-[10px] uppercase tracking-wider text-green-300 font-bold">Completed</div>
            <div className="text-xl font-black mt-1 text-green-300">{completedSteps}</div>
          </div>
          <div className="rounded-xl bg-red-500/10 border border-red-500/20 p-4">
            <div className="text-[10px] uppercase tracking-wider text-red-300 font-bold">Failed</div>
            <div className="text-xl font-black mt-1 text-red-300">{failedSteps}</div>
          </div>
          <div className="rounded-xl bg-white/5 border border-white/10 p-4">
            <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold">Total Duration</div>
            <div className="text-xl font-black mt-1">{totalDurationMs} ms</div>
          </div>
        </div>
      </div>

      <div className="glass rounded-[2rem] border border-white/10 p-8">
        <div className="flex items-center gap-3 mb-4">
          <Activity className="w-5 h-5 text-primary" />
          <h3 className="text-xl font-black">Score Breakdown</h3>
        </div>
        <pre className="text-xs text-primary/80 bg-black/30 rounded-xl p-4 overflow-x-auto whitespace-pre-wrap">
          {safeStringify(data.score_breakdown || {})}
        </pre>
      </div>

      {trace.length === 0 ? (
        <div className="glass rounded-[2rem] border border-white/10 p-10 text-center">
          <AlertTriangle className="w-10 h-10 text-amber-400 mx-auto mb-3" />
          <p className="text-muted-foreground">No workflow trace found for this report.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {trace.map((step: WorkflowTraceStep, index) => (
            <motion.div
              key={`${step.step}-${index}`}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.04 }}
              className="glass rounded-[2rem] border border-white/10 p-8"
            >
              <div className="text-[10px] mb-3 uppercase tracking-[0.2em] text-muted-foreground font-bold">
                Step {index + 1}
              </div>

              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
                    <StepIcon step={step.step} />
                  </div>
                  <div>
                    <h4 className="text-lg font-black">{step.node}</h4>
                    <p className="text-xs text-muted-foreground uppercase tracking-wider">{step.step}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-xs px-3 py-1 rounded-full border border-primary/20 bg-primary/10 text-primary font-bold">
                    model: {step.model}
                  </span>
                  <span className="text-xs px-3 py-1 rounded-full border border-white/15 bg-white/5 text-white/80 font-bold">
                    source: {step.source}
                  </span>
                  <span
                    className={`text-xs px-3 py-1 rounded-full border font-bold ${
                      step.status === "completed"
                        ? "border-green-500/20 bg-green-500/10 text-green-400"
                        : "border-red-500/20 bg-red-500/10 text-red-400"
                    }`}
                  >
                    {step.status === "completed" ? <CheckCircle2 className="w-3 h-3 inline mr-1" /> : null}
                    {step.status}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold mb-2">Input Passed</div>
                  <pre className="text-xs bg-black/30 rounded-xl p-4 overflow-x-auto whitespace-pre-wrap text-white/85">
                    {safeStringify(step.input || {})}
                  </pre>
                </div>

                <div>
                  <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold mb-2">Output Produced</div>
                  <pre className="text-xs bg-black/30 rounded-xl p-4 overflow-x-auto whitespace-pre-wrap text-primary/85">
                    {safeStringify(step.output || {})}
                  </pre>
                </div>
              </div>

              <div className="mt-4 text-[11px] text-muted-foreground flex flex-wrap gap-4">
                <span>started: {step.started_at}</span>
                <span>ended: {step.ended_at}</span>
                <span>duration: {step.duration_ms} ms</span>
              </div>

              {step.note ? <div className="mt-3 text-xs text-white/70">{step.note}</div> : null}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};

export default WorkflowTrace;
