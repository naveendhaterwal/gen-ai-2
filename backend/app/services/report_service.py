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
		"""Build a complete JSON report from workflow state aligned with PredictionResponse schema."""
		risk = state.risk_analysis or {}
		decision = state.final_decision or {}

		# Policy Retrieval format
		policy_matches_list = [
			{
				"rule_name": p["rule_name"],
				"rule_text": p["rule_text"],
				"status": p["status"],
				"source": p.get("source"),
				"score": p.get("score"),
			}
			for p in state.policy_matches
		]

		report = {
			"borrower_name": state.borrower_input.full_name if state.borrower_input else "Unknown",
			"request_id": state.request_id,
			"risk_analysis": {
				"risk_level": state.ml_risk_level.value if state.ml_risk_level else "Medium",
				"risk_score": state.ml_risk_score,
				"top_risk_factors": risk.get("top_risk_factors", []),
				"positive_factors": risk.get("positive_factors", []),
				"confidence_score": state.ml_confidence,
			},
			"policy_retrieval": {
				"rules_checked": len(state.policy_matches),
				"policies_matched": policy_matches_list,
			},
			"lending_decision": {
				"recommendation": decision.get("recommendation", "Manual Review"),
				"primary_reason": decision.get("primary_reason", "Policy analysis complete"),
				"secondary_reasons": decision.get("secondary_reasons", []),
				"suggested_action": decision.get("suggested_action", "Proceed with manual review"),
				"manual_review_needed": decision.get("manual_review_needed", True),
			},
			"foir": state.foir,
			"dti": state.dti,
			"proposed_emi": state.proposed_emi,
			"agent_interactions": state.agent_interactions,
			"score_breakdown": state.score_breakdown,
			"workflow_trace": state.workflow_trace,
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
