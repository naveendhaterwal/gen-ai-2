"""
Prediction Routes
Main endpoint: POST /predict-risk
Receives borrower data → runs workflow → returns decision.
"""

import logging
from fastapi import APIRouter, HTTPException

from app.schemas.borrower import BorrowerInput
from app.schemas.response import (
    PredictionResponse,
    RiskAnalysisResponse,
    PolicyRetrievalResponse,
    PolicyMatch,
    LendingDecisionResponse,
    RiskLevel,
    RecommendationType
)
from app.graph.workflow import run_credit_risk_workflow
from app.services.report_service import report_service

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/predict", tags=["Predictions"])


@router.post("/risk", response_model=PredictionResponse)
async def predict_risk(borrower_input: BorrowerInput) -> PredictionResponse:
    """
    Main prediction endpoint.
    
    Receives borrower form data, runs the multi-agent workflow,
    and returns complete credit risk assessment.
    
    Flow:
    1. Receive borrower input
    2. Calculate financial metrics (FOIR, DTI, EMI)
    3. ML model predicts risk
    4. LLM analyzes risk factors
    5. Check policies
    6. LLM makes decision
    7. Return complete report
    
    Args:
        borrower_input: Borrower data from form
        
    Returns:
        PredictionResponse with complete assessment
    """
    
    try:
        logger.info(f"📨 Received prediction request for {borrower_input.full_name}")
        
        # Run the workflow
        workflow_state = await run_credit_risk_workflow(borrower_input)
        
        # Log workflow issues but continue if core outputs exist.
        if workflow_state.errors:
            logger.warning(f"Workflow completed with errors: {workflow_state.errors}")

        if not workflow_state.ml_risk_level:
            raise HTTPException(
                status_code=500,
                detail="ML prediction did not return risk level"
            )
        
        # ========== BUILD RESPONSE ==========
        
        # Risk Analysis Response
        risk_data = workflow_state.risk_analysis or {}
        top_risk_factors = risk_data.get("top_risk_factors")
        positive_factors = risk_data.get("positive_factors")

        if not isinstance(top_risk_factors, list):
            top_risk_factors = []
        if not isinstance(positive_factors, list):
            positive_factors = []

        confidence_score = risk_data.get("confidence_score", workflow_state.ml_confidence)
        try:
            confidence_score = float(confidence_score)
        except (TypeError, ValueError):
            confidence_score = float(workflow_state.ml_confidence)

        risk_analysis = RiskAnalysisResponse(
            risk_level=workflow_state.ml_risk_level,
            risk_score=workflow_state.ml_risk_score,
            top_risk_factors=top_risk_factors,
            positive_factors=positive_factors,
            confidence_score=max(0.0, min(1.0, confidence_score))
        )
        
        # Policy Retrieval Response
        policy_matches_list = [
            PolicyMatch(
                rule_name=p["rule_name"],
                rule_text=p["rule_text"],
                status=p["status"],
                source=p.get("source"),
                score=p.get("score"),
            )
            for p in workflow_state.policy_matches
        ]
        
        policy_retrieval = PolicyRetrievalResponse(
            rules_checked=len(workflow_state.policy_matches),
            policies_matched=policy_matches_list
        )
        
        # Lending Decision Response
        decision_data = workflow_state.final_decision or {}

        recommendation_raw = decision_data.get("recommendation")
        valid_recommendations = {item.value for item in RecommendationType}

        if recommendation_raw not in valid_recommendations:
            if workflow_state.policy_violations >= 2:
                recommendation_raw = RecommendationType.REJECT.value
            elif workflow_state.policy_violations == 1:
                recommendation_raw = RecommendationType.REVIEW.value
            else:
                recommendation_raw = RecommendationType.APPROVE.value

        primary_reason = decision_data.get("primary_reason")
        if not primary_reason:
            primary_reason = f"Policy violations found: {workflow_state.policy_violations}"

        suggested_action = decision_data.get("suggested_action")
        if not suggested_action:
            if recommendation_raw == RecommendationType.REJECT.value:
                suggested_action = "Reject application based on current policy checks"
            elif recommendation_raw == RecommendationType.REVIEW.value:
                suggested_action = "Send application for manual credit review"
            else:
                suggested_action = "Proceed with standard approval process"

        secondary_reasons = decision_data.get("secondary_reasons", [])
        if not isinstance(secondary_reasons, list):
            secondary_reasons = []

        lending_decision = LendingDecisionResponse(
            recommendation=RecommendationType(recommendation_raw),
            primary_reason=primary_reason,
            secondary_reasons=secondary_reasons,
            suggested_action=suggested_action,
            manual_review_needed=bool(decision_data.get("manual_review_needed", recommendation_raw == RecommendationType.REVIEW.value))
        )
        
        # Build complete response
        response = PredictionResponse(
            borrower_name=borrower_input.full_name,
            request_id=workflow_state.request_id,
            risk_analysis=risk_analysis,
            policy_retrieval=policy_retrieval,
            lending_decision=lending_decision,
            foir=workflow_state.foir,
            dti=workflow_state.dti,
            proposed_emi=workflow_state.proposed_emi
        )
        
        logger.info(f"✓ Prediction complete for {borrower_input.full_name}")
        logger.info(f"  Request ID: {workflow_state.request_id}")
        logger.info(f"  Risk Level: {risk_analysis.risk_level}")
        logger.info(f"  Recommendation: {lending_decision.recommendation}")

        # Store a report snapshot for /api/report/{request_id} retrieval.
        report_service.save_report(report_service.build_report(workflow_state))
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error in prediction: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/health")
async def prediction_health():
    """Check if prediction service is ready"""
    return {
        "status": "healthy",
        "service": "prediction",
        "message": "Prediction service is running"
    }


@router.get("/info")
async def prediction_info():
    """Get info about prediction service"""
    return {
        "endpoint": "/api/predict/risk",
        "method": "POST",
        "description": "Assess borrower credit risk using ML + AI agents",
        "workflow_steps": [
            "Input Processing (calculate FOIR, DTI, EMI)",
            "ML Prediction (predict risk level)",
            "Risk Analysis (LLM explains risk factors)",
            "Policy Retrieval (check banking policies)",
            "Lending Decision (LLM makes recommendation)"
        ],
        "input_schema": BorrowerInput.schema(),
        "output_schema": PredictionResponse.schema()
    }
