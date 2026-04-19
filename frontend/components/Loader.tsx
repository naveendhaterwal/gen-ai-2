"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { BrainCircuit, Search, Database, ShieldCheck, CheckCircle2 } from "lucide-react";

const steps = [
  { id: 1, text: "Processing borrower data...", icon: <Search className="w-5 h-5" /> },
  { id: 2, text: "Consulting ML prediction model...", icon: <Database className="w-5 h-5" /> },
  { id: 3, text: "Retrieving RBI & SBI policies via RAG...", icon: <Search className="w-5 h-5" /> },
  { id: 4, text: "Analyzing compliance & risk factors...", icon: <BrainCircuit className="w-5 h-5" /> },
  { id: 5, text: "Generating final recommendation...", icon: <ShieldCheck className="w-5 h-5" /> },
];

const Loader = () => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center py-20 min-h-[400px]">
      <div className="relative mb-12">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
          className="w-32 h-32 border-4 border-primary/20 border-t-primary rounded-full"
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <BrainCircuit className="w-12 h-12 text-primary animate-pulse" />
        </div>
      </div>

      <div className="w-full max-w-md space-y-4">
        {steps.map((step, index) => (
          <motion.div
            key={step.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ 
              opacity: index <= currentStep ? 1 : 0.2,
              x: 0,
              scale: index === currentStep ? 1.05 : 1
            }}
            className="flex items-center gap-4 bg-white/5 border border-white/10 p-4 rounded-2xl"
          >
            <div className={index < currentStep ? "text-green-400" : index === currentStep ? "text-primary" : "text-muted-foreground"}>
              {index < currentStep ? <CheckCircle2 className="w-5 h-5" /> : step.icon}
            </div>
            <span className="text-sm font-medium tracking-wide">
              {step.text}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Loader;
