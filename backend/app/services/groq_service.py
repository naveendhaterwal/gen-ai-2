"""
Groq LLM Service
Handles calls to Groq API for AI agent responses.
"""

import logging
import json
from typing import Optional

from groq import Groq
from app.core.config import settings

logger = logging.getLogger(__name__)


class GroqService:
    """
    Service for interacting with Groq LLM.
    Used by AI agents to generate analysis and decisions.
    """
    
    def __init__(self):
        """Initialize Groq client"""
        self.client = None
        self.model = settings.GROQ_MODEL
        self._initialize_client()
    
    def _initialize_client(self):
        """Create Groq client"""
        try:
            if not settings.GROQ_API_KEY:
                logger.warning("GROQ_API_KEY not set in environment")
                return
            
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("✓ Groq client initialized")
            
        except Exception as e:
            logger.error(f"Error initializing Groq client: {str(e)}")
            self.client = None
    
    def call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> str:
        """
        Call Groq LLM with a prompt.
        
        Args:
            prompt: User message
            system_prompt: System context
            temperature: Creativity (0=deterministic, 1=creative)
            max_tokens: Max response length
            
        Returns:
            Response text from LLM
        """
        
        try:
            # Strict mode: caller decides fallback behavior.
            if not self.client:
                raise RuntimeError("Groq client not initialized")
            
            # Build messages
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.95,
                stream=False
            )
            
            # Extract response text
            result = response.choices[0].message.content
            
            logger.info(f"LLM Response: {len(result)} characters")
            return result
            
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            raise


class RiskAnalysisAgent:
    """Agent for analyzing credit risk"""
    
    def __init__(self, groq_service: GroqService):
        self.groq = groq_service
    
    def analyze(self, borrower_data: dict, risk_score: float, risk_level: str) -> dict:
        """
        Analyze risk factors for borrower.
        
        Returns dict with top_risk_factors, positive_factors, etc.
        """
        
        system_prompt = """You are a credit risk analyst. 
Analyze the borrower's profile and provide clear, concise risk factors.
Be specific and quantitative when possible.
Format as JSON."""
        
        user_prompt = f"""
Analyze this borrower's credit risk:
- Age: {borrower_data.get('age')}
- Credit Score: {borrower_data.get('credit_score')}
- Monthly Income: {borrower_data.get('monthly_income')}
- Employment: {borrower_data.get('employment_type')}
- FOIR: {borrower_data.get('foir')}
- DTI: {borrower_data.get('dti')}
- Loan Amount: {borrower_data.get('loan_amount_requested')}

ML Risk Score: {risk_score}
ML Risk Level: {risk_level}

Provide:
1. Top 3 risk factors
2. Top 2 positive factors
3. Confidence score (0-1)
"""
        
        try:
            response = self.groq.call_llm(user_prompt, system_prompt, temperature=0.2)
            result = json.loads(response)
            result["agent_source"] = "groq"
            result["warnings"] = []
            return result
        except Exception as exc:
            # Deterministic fallback without fabricated narrative text.
            risk_factors = []
            positive_factors = []

            if borrower_data.get("foir", 0.0) > 0.45:
                risk_factors.append("FOIR above 45% threshold")
            else:
                positive_factors.append("FOIR within threshold")

            if borrower_data.get("dti", 0.0) > 0.40:
                risk_factors.append("DTI above 40% threshold")
            else:
                positive_factors.append("DTI within threshold")

            credit_score = int(borrower_data.get("credit_score", 0))
            if credit_score < 600:
                risk_factors.append("Credit score below 600")
            elif credit_score >= 700:
                positive_factors.append("Credit score is strong")

            if not risk_factors:
                risk_factors.append("No major threshold breach detected")

            if not positive_factors:
                positive_factors.append("Limited positive factors from current threshold checks")

            return {
                "top_risk_factors": risk_factors,
                "positive_factors": positive_factors,
                "confidence_score": 0.70,
                "agent_source": "fallback",
                "warnings": [f"Risk analysis fallback used: {exc}"],
            }


class LendingDecisionAgent:
    """Agent for making lending decisions"""
    
    def __init__(self, groq_service: GroqService):
        self.groq = groq_service
    
    def decide(
        self,
        risk_analysis: dict,
        policy_matches: list,
        borrower_data: dict
    ) -> dict:
        """
        Make final lending decision based on risk and policies.
        
        Returns dict with recommendation, reasoning, etc.
        """
        
        system_prompt = """You are a lending decision expert.
Make clear, justifiable lending decisions.
Consider both risk and policy compliance.
Format as JSON."""
        
        user_prompt = f"""
Make a lending decision for:
Risk Factors: {json.dumps(risk_analysis.get('top_risk_factors', []))}
Positive Factors: {json.dumps(risk_analysis.get('positive_factors', []))}
FOIR: {borrower_data.get('foir')}
DTI: {borrower_data.get('dti')}
Credit Score: {borrower_data.get('credit_score')}

Policy Violations: {len([p for p in policy_matches if p.get('status') == 'Violated'])}

Options: Approve, Approve with Lower Amount, Manual Review, Reject

Provide:
1. Recommendation (one of the above)
2. Primary reason
3. Secondary reasons (list)
4. Suggested next action
"""
        
        try:
            response = self.groq.call_llm(user_prompt, system_prompt, temperature=0.2)
            result = json.loads(response)
            result["agent_source"] = "groq"
            result["warnings"] = []
            return result
        except Exception as exc:
            violations = len([p for p in policy_matches if p.get("status") == "Violated"])
            if violations >= 2:
                recommendation = "Reject"
                reason = "Multiple policy violations detected"
                action = "Reject application under current policy conditions"
                manual_review_needed = False
            elif violations == 1:
                recommendation = "Manual Review"
                reason = "Single policy violation requires underwriter review"
                action = "Route case to manual underwriting"
                manual_review_needed = True
            else:
                recommendation = "Approve"
                reason = "No policy violations detected"
                action = "Proceed with standard approval workflow"
                manual_review_needed = False

            return {
                "recommendation": recommendation,
                "primary_reason": reason,
                "secondary_reasons": [],
                "suggested_action": action,
                "manual_review_needed": manual_review_needed,
                "agent_source": "fallback",
                "warnings": [f"Decision fallback used: {exc}"],
            }


# Global instances
groq_service = GroqService()
risk_agent = RiskAnalysisAgent(groq_service)
decision_agent = LendingDecisionAgent(groq_service)
