export interface BorrowerInput {
  full_name: string;
  age: number;
  monthly_income: number;
  employment_type: "Salaried" | "Self-Employed" | "Business";
  credit_score: number;
  existing_loan_amount?: number;
  existing_emi_monthly?: number;
  loan_amount_requested: number;
  loan_purpose: "Home" | "Auto" | "Personal" | "Business";
  loan_tenure_months?: number;
}

export interface RiskAnalysis {
  risk_level: string;
  risk_score: number;
  top_risk_factors: string[];
  positive_factors: string[];
  confidence_score: number;
}

export interface PolicyMatch {
  rule_name: string;
  rule_text: string;
  status: "Passed" | "Failed" | "Warning";
  source?: string;
  score?: number;
}

export interface PredictionResponse {
  borrower_name: string;
  request_id: string;
  risk_analysis: RiskAnalysis;
  policy_retrieval: {
    rules_checked: number;
    policies_matched: PolicyMatch[];
  };
  lending_decision: {
    recommendation: "Approve" | "Approve with Lower Amount" | "Manual Review" | "Reject";
    primary_reason: string;
    secondary_reasons: string[];
    suggested_action: string;
    manual_review_needed: boolean;
  };
  foir: number;
  dti: number;
  proposed_emi: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function predictRisk(data: BorrowerInput): Promise<PredictionResponse> {
  const response = await fetch(`${API_BASE_URL}/predict/risk`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    let errorMessage = "Prediction failed";
    
    if (errorData.detail) {
      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      } else if (Array.isArray(errorData.detail)) {
        errorMessage = errorData.detail
          .map((err: any) => `${err.loc.join(".")}: ${err.msg}`)
          .join(", ");
      } else {
        errorMessage = JSON.stringify(errorData.detail);
      }
    }
    
    throw new Error(errorMessage);
  }

  return response.json();
}

export async function getReport(requestId: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/report/${requestId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch report");
  }
  return response.json();
}
