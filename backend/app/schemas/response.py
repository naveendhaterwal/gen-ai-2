"""
Response Schemas - Data models for API responses.
Defines what the frontend receives.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class RiskLevel(str, Enum):
    """Credit risk classification levels"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class RecommendationType(str, Enum):
    """Lending decision recommendation"""
    APPROVE = "Approve"
    APPROVE_LOWER = "Approve with Lower Amount"
    REVIEW = "Manual Review"
    REJECT = "Reject"


class RiskAnalysisResponse(BaseModel):
    """
    Risk analysis from the Risk Analysis Agent.
    Explains WHY the borrower is risky or safe.
    """
    
    risk_level: RiskLevel
    risk_score: float = Field(..., ge=0, le=100)
    top_risk_factors: List[str] = Field(
        ..., 
        description="Top 3-5 reasons why borrower is risky"
    )
    positive_factors: List[str] = Field(
        ..., 
        description="Positive factors working in borrower's favor"
    )
    confidence_score: float = Field(
        ..., 
        ge=0, 
        le=1, 
        description="Confidence of risk assessment (0-1)"
    )
    final_ai_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        description="Final synthesized risk score from AI agent"
    )
    ai_score_reasoning: Optional[str] = Field(
        default=None,
        description="Detailed reasoning for the final AI score"
    )


class PolicyMatch(BaseModel):
    """Single policy retrieved from knowledge base"""
    
    rule_name: str
    rule_text: str
    status: str = Field(..., description="Compliant, Borderline, or Violated")
    source: Optional[str] = Field(default=None, description="qdrant or fallback")
    score: Optional[str] = Field(default=None, description="retrieval relevance score")


class PolicyRetrievalResponse(BaseModel):
    """
    Policies retrieved from RAG system.
    Shows which lending rules were checked.
    """
    
    rules_checked: int
    policies_matched: List[PolicyMatch]


class LendingDecisionResponse(BaseModel):
    """
    Final lending decision from the Decision Agent.
    What should the bank do?
    """
    
    recommendation: RecommendationType
    primary_reason: str
    secondary_reasons: List[str] = []
    suggested_action: str = Field(
        ..., 
        description="What bank should do next"
    )
    manual_review_needed: bool = Field(
        default=False,
        description="Does this need human review?"
    )


class PredictionResponse(BaseModel):
    """
    Complete response from /predict-risk endpoint.
    Everything the frontend needs to show results.
    """
    
    # Request Info
    borrower_name: str
    request_id: str = Field(description="Unique request ID for tracking")
    
    # Risk Analysis
    risk_analysis: RiskAnalysisResponse
    
    # Policy Retrieved
    policy_retrieval: PolicyRetrievalResponse
    
    # Decision
    lending_decision: LendingDecisionResponse
    
    # Key Metrics
    foir: float = Field(..., description="Fixed Obligation to Income Ratio")
    dti: float = Field(..., description="Debt-to-Income Ratio")
    proposed_emi: float = Field(..., description="Proposed monthly EMI")
    
    agent_interactions: List[Dict[str, Any]] = Field(default_factory=list, description="AI Agent interaction logs")
    score_breakdown: Dict[str, Any] = Field(default_factory=dict, description="How risk score was computed")
    workflow_trace: List[Dict[str, Any]] = Field(default_factory=list, description="Step-by-step backend execution trace")
    
    class Config:
        json_schema_extra = {
            "example": {
                "borrower_name": "Rajesh Kumar",
                "request_id": "REQ_2024_001",
                "risk_analysis": {
                    "risk_level": "Medium",
                    "risk_score": 65,
                    "top_risk_factors": [
                        "High EMI burden (FOIR > 45%)",
                        "Moderate credit score",
                        "Large loan amount requested"
                    ],
                    "positive_factors": [
                        "Stable salaried employment",
                        "Consistent income"
                    ],
                    "confidence_score": 0.82
                },
                "policy_retrieval": {
                    "rules_checked": 8,
                    "policies_matched": []
                },
                "lending_decision": {
                    "recommendation": "Manual Review",
                    "primary_reason": "FOIR exceeds policy threshold",
                    "secondary_reasons": ["Income verification needed"],
                    "suggested_action": "Request additional income docs",
                    "manual_review_needed": True
                },
                "foir": 0.48,
                "dti": 0.15,
                "proposed_emi": 8000,
                "score_breakdown": {
                    "method": "ml_model",
                    "formula": "risk_score = P(default) * 100",
                    "default_probability": 0.65
                },
                "workflow_trace": []
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = "healthy"
    version: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response format"""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = None
    request_id: Optional[str] = None
