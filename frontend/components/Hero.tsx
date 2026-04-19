"use client";

import React from "react";
import { motion } from "framer-motion";
import { ArrowRight, BrainCircuit } from "lucide-react";

const Hero = ({ onStart }: { onStart: () => void }) => {
  return (
    <section className="relative pt-44 pb-20 overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[600px] bg-primary/10 blur-[120px] rounded-full -z-10 animate-pulse-slow" />
      
      <div className="container mx-auto px-6">
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto">
          {/* Badge */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 text-primary/80 text-[10px] font-bold uppercase tracking-[0.2em] mb-12 shadow-inner"
          >
            <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
            AI Prediction v2.0 is now live
          </motion.div>

          {/* Title */}
          <motion.h1
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.1, duration: 0.8 }}
            className="text-6xl md:text-8xl font-black tracking-tight mb-8 leading-[1]"
          >
            Predict Borrower Risk <br />
            <span className="text-muted-foreground/40">with Precision.</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.8 }}
            className="text-lg md:text-xl text-muted-foreground mb-12 max-w-2xl leading-relaxed"
          >
            Stop bad loans before they happen. Our advanced AI model analyzes 
            10+ behavioral metrics and banking policies with 99% accuracy.
          </motion.p>

          {/* CTA */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            <button
              onClick={onStart}
              className="bg-white text-black hover:bg-white/90 px-10 py-4 rounded-full text-lg font-black transition-all flex items-center gap-2 group shadow-2xl active:scale-95"
            >
              Get Started Free
            </button>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
