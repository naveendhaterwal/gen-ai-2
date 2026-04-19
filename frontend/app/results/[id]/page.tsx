"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { PredictionResponse, getReport } from "@/lib/api";
import ResultsDashboard from "@/components/ResultsDashboard";
import AIAgentLogs from "@/components/AIAgentLogs";
import ViewToggle from "@/components/ViewToggle";
import Loader from "@/components/Loader";
import { motion, AnimatePresence } from "framer-motion";
import { RefreshCcw, ChevronLeft, AlertCircle } from "lucide-react";

export default function ResultsPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"dashboard" | "agents">("dashboard");

  useEffect(() => {
    async function fetchReport() {
      if (!id) return;
      try {
        setLoading(true);
        const data = await getReport(id);
        setResult(data);
      } catch (err: any) {
        console.error("Failed to fetch report:", err);
        setError(err.message || "Could not retrieve assessment result.");
      } finally {
        setLoading(false);
      }
    }
    fetchReport();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-black relative">
        <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.05),transparent_50%)] pointer-events-none" />
        <Loader />
        <p className="mt-8 text-muted-foreground animate-pulse font-medium tracking-widest uppercase text-[10px]">Syncing with AI Agents...</p>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-black px-6 relative">
        <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.05),transparent_50%)] pointer-events-none" />
        <div className="max-w-md w-full glass p-10 border-red-500/20 rounded-[2.5rem] text-center relative z-10">
            <div className="w-16 h-16 bg-red-500/10 text-red-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <AlertCircle className="w-8 h-8" />
            </div>
          <h1 className="text-2xl font-bold mb-4">Error Loading Report</h1>
          <p className="text-muted-foreground mb-8 text-sm">{error || "The requested report could not be found."}</p>
          <button 
            onClick={() => router.push("/")}
            className="bg-white text-black px-8 py-3 rounded-full font-bold hover:bg-white/90 transition-all active:scale-95 flex items-center gap-2 mx-auto text-sm"
          >
            <ChevronLeft className="w-4 h-4" />
            Back to Assessment
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white selection:bg-primary/30 py-32 px-6 relative overflow-x-hidden">
      {/* Background Decor */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.02),transparent_70%)] pointer-events-none" />
      
      <div className="container mx-auto relative z-10">
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="flex flex-col md:flex-row items-center justify-between mb-16 gap-6"
        >
          <div className="flex items-center gap-5">
             <button 
                onClick={() => router.push("/")}
                className="w-12 h-12 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/5 transition-colors group"
                title="Back to Form"
             >
                <ChevronLeft className="w-6 h-6 group-hover:-translate-x-0.5 transition-transform" />
             </button>
             <div>
                <div className="text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-1">Assessment Generated</div>
                <h1 className="text-3xl md:text-4xl font-black tracking-tight">Risk Profile: {result.borrower_name}</h1>
             </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="hidden lg:block text-right mr-4">
                <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em]">Request ID</div>
                <div className="text-xs font-mono text-primary/60">{result.request_id}</div>
            </div>
            <button 
                onClick={() => router.push("/")}
                className="flex items-center gap-2 text-xs font-bold text-primary hover:text-primary/80 transition-colors bg-primary/10 px-8 py-4 rounded-full border border-primary/20 shadow-lg shadow-primary/5"
            >
                <RefreshCcw className="w-4 h-4" />
                New Analysis
            </button>
          </div>
        </motion.div>

        {/* Tab Toggle */}
        <ViewToggle activeTab={activeTab} onChange={setActiveTab} />

        <div className="relative pb-24">
          <AnimatePresence mode="wait">
            {activeTab === "dashboard" ? (
              <motion.div
                key="dashboard"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.3 }}
              >
                <ResultsDashboard data={result} />
              </motion.div>
            ) : (
              <motion.div
                key="agents"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
                className="max-w-4xl mx-auto"
              >
                <AIAgentLogs interactions={result.agent_interactions} />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
