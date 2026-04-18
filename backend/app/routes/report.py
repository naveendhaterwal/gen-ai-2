"""
Report Routes
Generate and retrieve structured lending reports.
"""

from fastapi import APIRouter, HTTPException

from app.graph.workflow import run_credit_risk_workflow
from app.schemas.borrower import BorrowerInput
from app.services.report_service import report_service


router = APIRouter(prefix="/report", tags=["Reports"])


@router.post("/generate")
async def generate_report(borrower_input: BorrowerInput):
	"""Generate a structured JSON report for one borrower case."""
	state = await run_credit_risk_workflow(borrower_input)
	if not state.request_id:
		raise HTTPException(status_code=500, detail="Failed to generate report request id")

	report = report_service.build_report(state)
	report_service.save_report(report)
	return report


@router.post("/generate-report")
async def generate_report_alias(borrower_input: BorrowerInput):
	"""Alias for compatibility with expected endpoint name."""
	return await generate_report(borrower_input)


@router.get("/{request_id}")
async def get_report(request_id: str):
	"""Fetch cached report by request id."""
	report = report_service.get_report(request_id)
	if not report:
		raise HTTPException(status_code=404, detail="Report not found")
	return report
