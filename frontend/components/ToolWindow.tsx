"use client";

import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ToolWindowProps {
  children: React.ReactNode;
  title?: string;
  className?: string;
}

const ToolWindow = ({ children, title = "app.creditrisk.ai/predict", className }: ToolWindowProps) => {
  return (
    <motion.div
      initial={{ y: 40, opacity: 0 }}
      whileInView={{ y: 0, opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className={cn(
        "glass border border-white/10 rounded-[2.5rem] overflow-hidden shadow-2xl shadow-primary/5 mx-auto max-w-5xl",
        className
      )}
    >
      {/* Browser Header */}
      <div className="bg-white/5 border-b border-white/10 px-6 py-4 flex items-center justify-between">
        <div className="flex gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500/50" />
          <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
          <div className="w-3 h-3 rounded-full bg-green-500/50" />
        </div>
        <div className="bg-black/40 px-4 py-1.5 rounded-lg border border-white/5 text-[10px] text-muted-foreground font-mono tracking-wider">
          {title}
        </div>
        <div className="w-12 h-1" /> {/* Spacer */}
      </div>

      {/* Content Area */}
      <div className="relative p-6 md:p-10 bg-gradient-to-b from-transparent to-primary/5">
        {children}
      </div>
    </motion.div>
  );
};

export default ToolWindow;
