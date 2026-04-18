"""
LangGraph Workflow Orchestration
Defines the multi-agent workflow for credit risk assessment.

Workflow flow:
Input → ML Prediction → Risk Analysis → Policy Retrieval → Decision → Output
"""

import logging
import json
import uuid
from datetime import datetime
from typing import Dict, Any

from langgraph.graph import StateGraph, END
from app.graph.state import WorkflowState
from app.schemas.borrower import BorrowerInput, BorrowerProfile
from app.schemas.response import RiskLevel
from app.services.ml_service import ml_service
from app.services.groq_service import groq_service, risk_agent, decision_agent
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)


def _normalize_workflow_state(raw_state: Any) -> WorkflowState:
    """Normalize workflow output to WorkflowState for compatibility."""
    if isinstance(raw_state, WorkflowState):
        return raw_state

    if isinstance(raw_state, dict):
        normalized = WorkflowState()
        for field_name in WorkflowState.__dataclass_fields__.keys():
            if field_name in raw_state:
                setattr(normalized, field_name, raw_state[field_name])
        return normalized

    raise TypeError(f"Unexpected workflow state type: {type(raw_state)}")


# ============================================================================
# NODE: INPUT PROCESSING & CALCULATIONS
# ============================================================================

def node_input_processing(state: WorkflowState) -> WorkflowState:
    """
    Process input and calculate financial metrics.
    
    Calculates:
    - FOIR (Fixed Obligation to Income Ratio)
    - DTI (Debt-to-Income Ratio)
    - Proposed EMI
    """
    
    logger.info("📥 Node: Input Processing")
    
    try:
        borrower = state.borrower_input
        
        # Extract values
        monthly_income = borrower.monthly_income
        existing_emi = borrower.existing_emi_monthly
        loan_amount = borrower.loan_amount_requested
        tenure_months = borrower.loan_tenure_months
        existing_loans = borrower.existing_loan_amount
        
        # Store in state
        state.monthly_income = monthly_income
        state.existing_emi_monthly = existing_emi
        state.loan_amount_requested = loan_amount
        state.loan_tenure_months = tenure_months
        
        # ========== CALCULATE PROPOSED EMI ==========
        # Formula: EMI = P * [r(1+r)^n] / [(1+r)^n - 1]
        # Where: P = Principal, r = monthly rate, n = tenure in months
        # Simplified: Using 10% annual rate as standard
        
        annual_rate = 0.10  # 10% per annum
        monthly_rate = annual_rate / 12
        
        if monthly_rate > 0:
            numerator = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months)
            denominator = ((1 + monthly_rate) ** tenure_months) - 1
            proposed_emi = numerator / denominator
        else:
            proposed_emi = loan_amount / tenure_months
        
        state.proposed_emi = round(proposed_emi, 2)
        
        logger.info(f"   Proposed EMI: ₹{state.proposed_emi:,.0f}")
        
        # ========== CALCULATE FOIR (Fixed Obligation to Income Ratio) ==========
        # FOIR = (Existing EMI + Proposed EMI) / Monthly Income
        # Banks prefer FOIR < 45%
        
        total_emi = existing_emi + proposed_emi
        state.total_emi_after_loan = round(total_emi, 2)
        
        if monthly_income > 0:
            foir = (total_emi / monthly_income) * 100
            state.foir = round(foir / 100, 4)  # Store as decimal (0.45 = 45%)
        else:
            state.foir = 0.0
        
        logger.info(f"   FOIR: {state.foir*100:.2f}%")
        
        # ========== CALCULATE DTI (Debt-to-Income Ratio) ==========
        # DTI = (Existing Loans + Requested Loan) / Monthly Income
        # Banks prefer DTI < 40%
        
        total_debt = existing_loans + loan_amount
        
        if monthly_income > 0:
            dti = (total_debt / monthly_income) * 100
            state.dti = round(dti / 100, 4)  # Store as decimal
        else:
            state.dti = 0.0
        
        logger.info(f"   DTI: {state.dti*100:.2f}%")
        
        # Create enriched borrower profile
        borrower_profile = BorrowerProfile(
            full_name=borrower.full_name,
            age=borrower.age,
            monthly_income=monthly_income,
            employment_type=borrower.employment_type,
            credit_score=borrower.credit_score,
            existing_loan_amount=existing_loans,
            existing_emi_monthly=existing_emi,
            loan_amount_requested=loan_amount,
            loan_purpose=borrower.loan_purpose,
            loan_tenure_months=tenure_months,
            foir=state.foir,
            dti=state.dti,
            proposed_emi=state.proposed_emi,
            total_emi_after_loan=state.total_emi_after_loan,
        )
        
        # Store in state (we'll need this for ML service)
        state.step_completed = "input_processing"
        logger.info("✓ Input processing complete")
        
        return state
        
    except Exception as e:
        logger.error(f"❌ Error in input processing: {str(e)}")
        state.add_error(f"Input processing failed: {str(e)}")
        state.step_completed = "input_processing_failed"
        return state


# ============================================================================
# NODE: ML PREDICTION
# ============================================================================

def node_ml_prediction(state: WorkflowState) -> WorkflowState:
    """
    Call ML service to predict credit risk.
    """
    
    logger.info("🤖 Node: ML Prediction")
    
    try:
        borrower = state.borrower_input
        
        # Create profile for ML service
        borrower_profile = BorrowerProfile(
            full_name=borrower.full_name,
            age=borrower.age,
            monthly_income=state.monthly_income,
            employment_type=borrower.employment_type,
            credit_score=borrower.credit_score,
            existing_loan_amount=borrower.existing_loan_amount,
            existing_emi_monthly=state.existing_emi_monthly,
            loan_amount_requested=state.loan_amount_requested,
            loan_purpose=borrower.loan_purpose,
            loan_tenure_months=state.loan_tenure_months,
            foir=state.foir,
            dti=state.dti,
            proposed_emi=state.proposed_emi,
            total_emi_after_loan=state.total_emi_after_loan,
        )
        
        # Get ML prediction
        risk_level_str, risk_score, confidence = ml_service.predict_risk(borrower_profile)
        
        # Convert to enum
        state.ml_risk_level = RiskLevel(risk_level_str)
        state.ml_risk_score = round(risk_score, 2)
        state.ml_confidence = round(confidence, 3)
        
        logger.info(f"   Risk Level: {state.ml_risk_level.value}")
        logger.info(f"   Risk Score: {state.ml_risk_score}")
        logger.info(f"   Confidence: {state.ml_confidence}")
        
        state.step_completed = "ml_prediction"
        logger.info("✓ ML prediction complete")
        
        return state
        
    except Exception as e:
        logger.error(f"❌ Error in ML prediction: {str(e)}")
        state.add_error(f"ML prediction failed: {str(e)}")
        state.step_completed = "ml_prediction_failed"
        return state


# ============================================================================
# NODE: RISK ANALYSIS AGENT
# ============================================================================

def node_risk_analysis(state: WorkflowState) -> WorkflowState:
    """
    Use LLM to analyze risk factors.
    Real Groq API call (no mocks).
    """
    
    logger.info("🔍 Node: Risk Analysis Agent")
    
    try:
        borrower = state.borrower_input
        
        # Build borrower data dict for LLM
        borrower_data = {
            "age": borrower.age,
            "credit_score": borrower.credit_score,
            "monthly_income": state.monthly_income,
            "employment_type": borrower.employment_type,
            "foir": state.foir,
            "dti": state.dti,
            "loan_amount_requested": state.loan_amount_requested,
            "existing_loans": borrower.existing_loan_amount
        }
        
        # Call the risk analysis agent
        analysis = risk_agent.analyze(
            borrower_data=borrower_data,
            risk_score=state.ml_risk_score,
            risk_level=state.ml_risk_level.value if state.ml_risk_level else "Unknown"
        )
        
        state.risk_analysis = analysis
        
        logger.info(f"   Top Risk Factors: {analysis.get('top_risk_factors', [])}")
        logger.info(f"   Positive Factors: {analysis.get('positive_factors', [])}")
        
        state.step_completed = "risk_analysis"
        logger.info("✓ Risk analysis complete")
        
        return state
        
    except Exception as e:
        logger.error(f"❌ Error in risk analysis: {str(e)}")
        state.add_error(f"Risk analysis failed: {str(e)}")
        state.step_completed = "risk_analysis_failed"
        return state


# ============================================================================
# NODE: POLICY RETRIEVAL
# ============================================================================

def node_policy_retrieval(state: WorkflowState) -> WorkflowState:
    """
    Retrieve applicable policies from knowledge base using RAG.
    """
    
    logger.info("📋 Node: Policy Retrieval")
    
    try:
        borrower = state.borrower_input
        borrower_context = {
            "age": borrower.age,
            "monthly_income": state.monthly_income,
            "employment_type": borrower.employment_type,
            "credit_score": borrower.credit_score,
            "loan_amount_requested": state.loan_amount_requested,
            "loan_purpose": borrower.loan_purpose,
            "foir": state.foir,
            "dti": state.dti,
        }

        retrieval_result = rag_service.retrieve_policies(borrower_context)
        policies = retrieval_result.get("policies", [])

        violations = sum(1 for p in policies if p.get("status") == "Violated")
        compliances = sum(1 for p in policies if p.get("status") == "Compliant")

        state.policy_matches = policies
        state.policy_violations = violations
        state.policy_compliances = compliances

        for warning in retrieval_result.get("warnings", []):
            state.add_error(warning)
        
        logger.info(f"   Policies Checked: {len(policies)}")
        logger.info(f"   Violations: {violations}, Compliances: {compliances}")
        
        state.step_completed = "policy_retrieval"
        logger.info("✓ Policy retrieval complete")
        
        return state
        
    except Exception as e:
        logger.error(f"❌ Error in policy retrieval: {str(e)}")
        state.add_error(f"Policy retrieval failed: {str(e)}")
        state.step_completed = "policy_retrieval_failed"
        return state


# ============================================================================
# NODE: LENDING DECISION
# ============================================================================

def node_lending_decision(state: WorkflowState) -> WorkflowState:
    """
    Use LLM to make final lending decision.
    Real Groq API call (no mocks).
    """
    
    logger.info("⚖️ Node: Lending Decision Agent")
    
    try:
        borrower = state.borrower_input
        
        # Build borrower data dict for decision agent
        borrower_data = {
            "age": borrower.age,
            "credit_score": borrower.credit_score,
            "monthly_income": state.monthly_income,
            "employment_type": borrower.employment_type,
            "foir": state.foir,
            "dti": state.dti,
            "loan_amount_requested": state.loan_amount_requested,
            "existing_loans": borrower.existing_loan_amount
        }
        
        # Call decision agent
        decision = decision_agent.decide(
            risk_analysis=state.risk_analysis,
            policy_matches=state.policy_matches,
            borrower_data=borrower_data
        )
        
        state.final_decision = decision
        
        logger.info(f"   Recommendation: {decision.get('recommendation')}")
        logger.info(f"   Reason: {decision.get('primary_reason')}")
        
        state.step_completed = "lending_decision"
        logger.info("✓ Lending decision complete")
        
        return state
        
    except Exception as e:
        logger.error(f"❌ Error in lending decision: {str(e)}")
        state.add_error(f"Lending decision failed: {str(e)}")
        state.step_completed = "lending_decision_failed"
        return state


# ============================================================================
# BUILD THE WORKFLOW GRAPH
# ============================================================================

def build_workflow():
    """
    Build and compile the LangGraph workflow.
    """
    
    # Create graph
    workflow = StateGraph(WorkflowState)
    
    # Add nodes (functions)
    workflow.add_node("input_processing", node_input_processing)
    workflow.add_node("ml_prediction", node_ml_prediction)
    workflow.add_node("risk_analysis", node_risk_analysis)
    workflow.add_node("policy_retrieval", node_policy_retrieval)
    workflow.add_node("lending_decision", node_lending_decision)
    
    # Set entry point
    workflow.set_entry_point("input_processing")
    
    # Add edges (flow)
    workflow.add_edge("input_processing", "ml_prediction")
    workflow.add_edge("ml_prediction", "risk_analysis")
    workflow.add_edge("risk_analysis", "policy_retrieval")
    workflow.add_edge("policy_retrieval", "lending_decision")
    workflow.add_edge("lending_decision", END)
    
    # Compile
    graph = workflow.compile()
    
    logger.info("✓ LangGraph workflow compiled successfully")
    
    return graph


# Create global workflow instance
credit_risk_workflow = build_workflow()


# ============================================================================
# RUN WORKFLOW
# ============================================================================

async def run_credit_risk_workflow(borrower_input: BorrowerInput) -> WorkflowState:
    """
    Execute the complete credit risk assessment workflow.
    
    Args:
        borrower_input: BorrowerInput from frontend form
        
    Returns:
        Final WorkflowState with all results
    """
    
    logger.info("=" * 80)
    logger.info("🚀 STARTING CREDIT RISK ASSESSMENT WORKFLOW")
    logger.info("=" * 80)
    
    # Create initial state
    initial_state = WorkflowState(
        borrower_input=borrower_input,
        request_id=f"REQ_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    )
    
    logger.info(f"Request ID: {initial_state.request_id}")
    logger.info(f"Borrower: {borrower_input.full_name}")
    
    # Run workflow
    try:
        final_state_raw = credit_risk_workflow.invoke(initial_state)
        final_state = _normalize_workflow_state(final_state_raw)
        
        logger.info("=" * 80)
        logger.info("✓ WORKFLOW COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
        return final_state
        
    except Exception as e:
        logger.error(f"❌ WORKFLOW FAILED: {str(e)}")
        initial_state.add_error(f"Workflow execution failed: {str(e)}")
        return initial_state
