"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { User, Wallet, Calculator, Briefcase, Info, Send } from "lucide-react";
import { BorrowerInput } from "@/lib/api";
import { cn } from "@/lib/utils";

interface BorrowerFormProps {
  onSubmit: (data: BorrowerInput) => void;
  isLoading: boolean;
}

const BorrowerForm = ({ onSubmit, isLoading }: BorrowerFormProps) => {
  const [formData, setFormData] = useState<Partial<BorrowerInput>>({
    employment_type: "Salaried",
    loan_purpose: "Personal",
    loan_tenure_months: 60,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? (value === "" ? "" : parseFloat(value)) : value,
    }));
  };

  const fillDemoData = () => {
    setFormData({
      full_name: "Rajesh Kumar",
      age: 35,
      employment_type: "Salaried",
      monthly_income: 85000,
      credit_score: 780,
      existing_loan_amount: 150000,
      existing_emi_monthly: 12000,
      loan_amount_requested: 500000,
      loan_purpose: "Personal",
      loan_tenure_months: 36,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData as BorrowerInput);
  };

  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="max-w-4xl mx-auto w-full"
    >
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Personal & Employment Section */}
        <FormSection title="Personal & Employment" icon={<User className="w-5 h-5" />}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <InputField
              label="Full Name"
              name="full_name"
              placeholder="e.g. Rajesh Kumar"
              required
              onChange={handleChange}
              value={formData.full_name || ""}
            />
            <InputField
              label="Age"
              name="age"
              type="number"
              placeholder="e.g. 35"
              required
              onChange={handleChange}
              value={formData.age || ""}
              min={18}
              max={70}
            />
            <SelectField
              label="Employment Type"
              name="employment_type"
              options={["Salaried", "Self-Employed", "Business"]}
              onChange={handleChange}
              value={formData.employment_type}
            />
            <InputField
              label="Monthly Income (₹)"
              name="monthly_income"
              type="number"
              placeholder="e.g. 50000"
              required
              onChange={handleChange}
              value={formData.monthly_income || ""}
            />
          </div>
        </FormSection>

        {/* Credit & Financial Section */}
        <FormSection title="Financial Health" icon={<Wallet className="w-5 h-5" />}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <InputField
              label="Credit Score (CIBIL)"
              name="credit_score"
              type="number"
              placeholder="300 - 900"
              required
              onChange={handleChange}
              value={formData.credit_score || ""}
              min={300}
              max={900}
            />
            <InputField
              label="Existing Total Loan Amount (₹)"
              name="existing_loan_amount"
              type="number"
              placeholder="e.g. 200000"
              onChange={handleChange}
              value={formData.existing_loan_amount || ""}
            />
            <InputField
              label="Current Total Monthly EMI (₹)"
              name="existing_emi_monthly"
              type="number"
              placeholder="e.g. 5000"
              onChange={handleChange}
              value={formData.existing_emi_monthly || ""}
            />
          </div>
        </FormSection>

        {/* Loan Request Section */}
        <FormSection title="Loan Details" icon={<Calculator className="w-5 h-5" />}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <InputField
              label="Loan Amount Requested (₹)"
              name="loan_amount_requested"
              type="number"
              placeholder="e.g. 500000"
              required
              onChange={handleChange}
              value={formData.loan_amount_requested || ""}
            />
            <SelectField
              label="Loan Purpose"
              name="loan_purpose"
              options={["Home", "Auto", "Personal", "Business"]}
              onChange={handleChange}
              value={formData.loan_purpose}
            />
            <InputField
              label="Loan Tenure (Months)"
              name="loan_tenure_months"
              type="number"
              placeholder="e.g. 60"
              required
              onChange={handleChange}
              value={formData.loan_tenure_months || ""}
            />
          </div>
        </FormSection>

        <div className="flex flex-col md:flex-row items-center justify-center gap-4 pt-8">
          <button
            type="button"
            onClick={fillDemoData}
            disabled={isLoading}
            className="px-8 py-4 rounded-2xl text-lg font-bold transition-all border border-white/10 hover:bg-white/5 active:scale-95 disabled:opacity-50"
          >
            Fill Demo Data
          </button>
          <button
            type="submit"
            disabled={isLoading}
            className={cn(
              "px-12 py-4 rounded-2xl text-lg font-bold transition-all flex items-center gap-3 shadow-xl",
              isLoading 
                ? "bg-white/10 text-muted-foreground cursor-not-allowed" 
                : "bg-primary hover:bg-primary/90 text-primary-foreground glow-blue hover:-translate-y-1"
            )}
          >
            {isLoading ? "Running Prediction Agents..." : "Run Risk Assessment"}
            {!isLoading && <Send className="w-5 h-5" />}
          </button>
        </div>
      </form>
    </motion.div>
  );
};

const FormSection = ({ title, icon, children }: { title: string; icon: React.ReactNode; children: React.ReactNode }) => (
  <div className="glass p-8 rounded-3xl border border-white/10 relative overflow-hidden group">
    <div className="absolute top-0 right-0 p-8 opacity-[0.03] group-hover:opacity-[0.07] transition-opacity">
      {icon}
    </div>
    <div className="flex items-center gap-3 mb-8">
      <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary">
        {icon}
      </div>
      <h3 className="text-xl font-bold tracking-tight">{title}</h3>
    </div>
    {children}
  </div>
);

const InputField = ({ label, ...props }: { label: string } & React.InputHTMLAttributes<HTMLInputElement>) => (
  <div className="space-y-2">
    <label className="text-sm font-medium text-muted-foreground ml-1">{label}</label>
    <input
      {...props}
      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-primary/50 focus:bg-white/[0.08] transition-all text-foreground placeholder:text-muted-foreground/30"
    />
  </div>
);

const SelectField = ({ label, options, name, value, onChange }: { label: string; options: string[]; name: string; value: any; onChange: any }) => (
  <div className="space-y-2">
    <label className="text-sm font-medium text-muted-foreground ml-1">{label}</label>
    <select
      name={name}
      value={value}
      onChange={onChange}
      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-primary/50 focus:bg-white/[0.08] transition-all text-foreground appearance-none cursor-pointer"
    >
      {options.map((opt) => (
        <option key={opt} value={opt} className="bg-zinc-900">
          {opt}
        </option>
      ))}
    </select>
  </div>
);

export default BorrowerForm;
