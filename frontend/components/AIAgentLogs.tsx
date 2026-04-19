"use client";

import React from "react";
import { motion } from "framer-motion";
import { AgentInteraction } from "@/lib/api";
import { Terminal, Bot, MessageSquare, ShieldAlert, Cpu } from "lucide-react";

interface AIAgentLogsProps {
  interactions: AgentInteraction[];
}

const AIAgentLogs: React.FC<AIAgentLogsProps> = ({ interactions }) => {
  if (!interactions || interactions.length === 0) {
    return (
      <div className="text-center py-20 glass rounded-[2.5rem] border-white/5">
        <Bot className="w-12 h-12 text-muted-foreground mx-auto mb-4 opacity-20" />
        <p className="text-muted-foreground">No agent interaction logs available.</p>
      </div>
    );
  }

  return (
    <div className="space-y-12">
      {interactions.map((interaction, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="relative"
        >
          {/* Connector Line */}
          {index < interactions.length - 1 && (
            <div className="absolute left-6 top-16 bottom-0 w-px bg-gradient-to-b from-primary/30 to-transparent" />
          )}

          <div className="flex gap-6">
            <div className="relative z-10">
              <div className="w-12 h-12 rounded-2xl bg-black border border-white/10 flex items-center justify-center shadow-2xl">
                {interaction.agent.includes("Risk") ? (
                  <ShieldAlert className="w-6 h-6 text-red-500" />
                ) : interaction.agent.includes("Decision") ? (
                  <Cpu className="w-6 h-6 text-primary" />
                ) : (
                  <Terminal className="w-6 h-6 text-muted-foreground" />
                )}
              </div>
            </div>

            <div className="flex-1 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-black tracking-tight">{interaction.agent}</h3>
                  <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mt-1">Thought Process Log</div>
                </div>
                {interaction.error && (
                  <div className="bg-red-500/10 text-red-500 text-[10px] font-bold px-3 py-1 rounded-full border border-red-500/20 uppercase tracking-tighter">
                    Fallback Mode
                  </div>
                )}
              </div>

              {/* Interaction Cards */}
              <div className="grid grid-cols-1 gap-4">
                {/* System/Prompt Section */}
                <div className="glass rounded-[1.5rem] overflow-hidden border-white/5">
                  <div className="bg-white/[0.03] px-6 py-3 border-b border-white/5 flex items-center gap-2">
                    <Terminal className="w-3 h-3 text-muted-foreground" />
                    <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">Input Prompt</span>
                  </div>
                  <div className="p-6">
                    <pre className="text-xs text-primary/70 font-mono whitespace-pre-wrap leading-relaxed">
                      {interaction.prompt}
                    </pre>
                  </div>
                </div>

                {/* Response Section */}
                <div className="glass rounded-[1.5rem] overflow-hidden border-primary/10 bg-primary/[0.02]">
                  <div className="bg-primary/5 px-6 py-3 border-b border-primary/10 flex items-center gap-2">
                    <MessageSquare className="w-3 h-3 text-primary" />
                    <span className="text-[10px] font-bold text-primary uppercase tracking-wider">Agent Response</span>
                  </div>
                  <div className="p-6">
                    <div className="text-sm text-white/90 leading-relaxed font-medium">
                      {interaction.response.startsWith('{') ? (
                        <pre className="font-mono text-xs text-white/80 whitespace-pre-wrap">
                          {JSON.stringify(JSON.parse(interaction.response), null, 2)}
                        </pre>
                      ) : (
                        interaction.response
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default AIAgentLogs;
