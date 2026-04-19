"use client";

import React, { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Hero from "@/components/Hero";
import BorrowerForm from "@/components/BorrowerForm";
import Loader from "@/components/Loader";
import ToolWindow from "@/components/ToolWindow";
import { FloatingRiskCard, FloatingAnalysisCard } from "@/components/FloatingCards";
import { BorrowerInput, predictRisk } from "@/lib/api";
import { ChevronLeft } from "lucide-react";
import { useRouter } from "next/navigation";

type WorkflowState = "IDLE" | "LOADING" | "RESULTS" | "ERROR";

export default function Home() {
  const router = useRouter();
  const [state, setState] = useState<WorkflowState>("IDLE");
  const [error, setError] = useState<string | null>(null);
  
  const toolRef = useRef<HTMLDivElement>(null);

  const scrollToTool = () => {
    toolRef.current?.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  const handleSubmit = async (data: BorrowerInput) => {
    setState("LOADING");
    setError(null);
    scrollToTool();
    
    try {
      const response = await predictRisk(data);
      router.push(`/results/${response.request_id}`);
    } catch (err: any) {
      console.error("Prediction failed:", err);
      setError(err.message || "An unexpected error occurred.");
      setState("ERROR");
    }
  };

  const reset = () => {
    setError(null);
    setState("IDLE");
    scrollToTool();
  };

  return (
    <div className="min-h-screen bg-black text-white selection:bg-primary/30 overflow-x-hidden">
      {/* Background Decor */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.05),transparent_50%)] pointer-events-none" />

      {/* Hero Section - Always Visible */}
      <Hero onStart={scrollToTool} />

      {/* Main Tool Area - Single Page Integration */}
      <section className="container mx-auto px-6 pb-44 relative" ref={toolRef}>
        <div className="relative">
          {/* Decorative Floating Cards */}
          <FloatingRiskCard 
            isHighRisk={false} 
          />
          <FloatingAnalysisCard 
            isCompliant={true} 
          />

          <ToolWindow>
            <AnimatePresence mode="wait">
              {state === "IDLE" && (
                <motion.div
                  key="form"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="space-y-8"
                >
                  <div className="mb-10 text-center md:text-left">
                    <h2 className="text-3xl font-black mb-2 tracking-tight">Borrower Assessment</h2>
                    <p className="text-muted-foreground text-sm">Enter the details below to evaluate creditworthiness in real-time.</p>
                  </div>
                  <BorrowerForm onSubmit={handleSubmit} isLoading={false} />
                </motion.div>
              )}

              {state === "LOADING" && (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <Loader />
                </motion.div>
              )}



              {state === "ERROR" && (
                <motion.div
                  key="error"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="py-20 text-center"
                >
                  <div className="max-w-md mx-auto p-10 glass border-red-500/20 rounded-[2rem]">
                    <div className="w-16 h-16 bg-red-500/10 text-red-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                      <ChevronLeft className="w-8 h-8" />
                    </div>
                    <h3 className="text-2xl font-bold mb-4">Assessment Failed</h3>
                    <p className="text-muted-foreground text-sm mb-8">{error}</p>
                    <button
                      onClick={reset}
                      className="bg-white text-black px-8 py-3 rounded-full font-bold hover:bg-white/90 transition-all active:scale-95"
                    >
                      Back to Form
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </ToolWindow>
        </div>
      </section>

      {/* Footer Branding */}
      <footer className="py-20 border-t border-white/5 text-center">
        <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.3em] mb-4">
          Powered by CR AI Neural Network
        </div>
        <div className="flex justify-center gap-8 opacity-20 grayscale">
          <div className="font-black">FINTECH</div>
          <div className="font-black">LENDING</div>
          <div className="font-black">NEURAL</div>
        </div>
      </footer>
    </div>
  );
}
