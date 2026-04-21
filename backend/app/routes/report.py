"""
Report Routes
Generate and retrieve structured lending reports.
"""

import logging
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel
from app.graph.workflow import run_credit_risk_workflow
from app.schemas.borrower import BorrowerInput
from app.services.report_service import report_service
from app.services.groq_service import chat_agent

logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    report_data: dict  # Full report sent from frontend — no server-side cache lookup needed


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

@router.post("/{request_id}/chat")
async def chat_with_report(request_id: str, chat_request: ChatRequest):
	"""Chat with the AI about a specific report.
	
	The full report is sent from the frontend in the request body,
	so this endpoint works regardless of which server worker handles the request.
	"""
	logger.info(f"💬 Chat request received for report ID: {request_id}")
	
	if not chat_request.report_data:
		logger.error(f"❌ No report_data in request body for ID: {request_id}")
		raise HTTPException(status_code=400, detail="report_data is required in the request body")
	
	logger.info(f"✅ Report data received from frontend. Sending to AI chat agent...")
	response = chat_agent.chat(chat_request.report_data, chat_request.message)
	return response
