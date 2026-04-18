"""
Report Service
Builds structured JSON report payloads and caches by request id.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from app.graph.state import WorkflowState


class ReportService:
	"""Service for building and retrieving structured borrower reports."""

	def __init__(self) -> None:
		self._cache: Dict[str, Dict[str, Any]] = {}

	def build_report(self, state: WorkflowState) -> Dict[str, Any]:
		"""Build a complete JSON report from workflow state."""
		borrower = state.borrower_input
		decision = state.final_decision or {}
		risk = state.risk_analysis or {}

		report = {
			"request_id": state.request_id,
			"generated_at": datetime.utcnow().isoformat(),
			"borrower_summary": {
				"full_name": borrower.full_name if borrower else "",
				"age": borrower.age if borrower else None,
				"monthly_income": borrower.monthly_income if borrower else None,
				"employment_type": borrower.employment_type if borrower else "",
				"credit_score": borrower.credit_score if borrower else None,
				"loan_amount_requested": borrower.loan_amount_requested if borrower else None,
				"loan_purpose": borrower.loan_purpose if borrower else "",
				"loan_tenure_months": borrower.loan_tenure_months if borrower else None,
			},
			"metrics": {
				"foir": state.foir,
				"dti": state.dti,
				"proposed_emi": state.proposed_emi,
				"total_emi_after_loan": state.total_emi_after_loan,
			},
			"risk_analysis": {
				"risk_level": state.ml_risk_level.value if state.ml_risk_level else None,
				"risk_score": state.ml_risk_score,
				"confidence": state.ml_confidence,
				"top_risk_factors": risk.get("top_risk_factors", []),
				"positive_factors": risk.get("positive_factors", []),
				"agent_source": risk.get("agent_source", "unknown"),
				"warnings": risk.get("warnings", []),
			},
			"policies": {
				"matches": state.policy_matches,
				"violations": state.policy_violations,
				"compliances": state.policy_compliances,
			},
			"decision": {
				"recommendation": decision.get("recommendation"),
				"primary_reason": decision.get("primary_reason"),
				"secondary_reasons": decision.get("secondary_reasons", []),
				"suggested_action": decision.get("suggested_action"),
				"manual_review_needed": decision.get("manual_review_needed", False),
				"agent_source": decision.get("agent_source", "unknown"),
				"warnings": decision.get("warnings", []),
			},
			"audit": {
				"step_completed": state.step_completed,
				"errors": state.errors,
			},
		}

		return report

	def save_report(self, report: Dict[str, Any]) -> None:
		"""Cache report by request_id."""
		request_id = report.get("request_id")
		if request_id:
			self._cache[request_id] = report

	def get_report(self, request_id: str) -> Dict[str, Any] | None:
		"""Retrieve cached report by request id."""
		return self._cache.get(request_id)


report_service = ReportService()
