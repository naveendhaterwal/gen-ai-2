"use client";

import React from "react";
import { motion } from "framer-motion";
import { Shield } from "lucide-react";
import { cn } from "@/lib/utils";

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex justify-center p-4">
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="glass flex items-center justify-between w-full max-w-6xl px-6 py-3 rounded-2xl border border-white/10 hover:border-white/20 transition-all duration-500"
      >
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-primary/20 rounded-xl flex items-center justify-center border border-primary/30">
            <Shield className="w-6 h-6 text-primary" />
          </div>
          <span className="text-xl font-bold tracking-tight">
            CR <span className="text-primary">AI</span>
          </span>
        </div>

        {/* Action Button */}
        <div className="flex items-center gap-4">
          <button className="bg-white text-black hover:bg-white/90 px-6 py-2 rounded-xl text-sm font-bold transition-all shadow-lg active:scale-95">
            Contact Sales
          </button>
        </div>
      </motion.div>
    </nav>
  );
};

export default Navbar;
