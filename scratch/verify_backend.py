import asyncio
import json
from app.graph.workflow import run_credit_risk_workflow
from app.schemas.borrower import BorrowerInput

async def test_workflow():
    test_input = BorrowerInput(
        full_name="Alice Verification",
        age=30,
        monthly_income=200000,
        employment_type="Salaried",
        credit_score=800,
        existing_loan_amount=0,
        existing_emi_monthly=0,
        loan_amount_requested=1000000,
        loan_purpose="Home",
        loan_tenure_months=60
    )
    
    print("Running workflow...")
    final_state = await run_credit_risk_workflow(test_input)
    
    print("\nAGENT INTERACTIONS LOGGED:")
    print(f"Count: {len(final_state.agent_interactions)}")
    
    for interaction in final_state.agent_interactions:
        print(f"\n--- AGENT: {interaction['agent']} ---")
        print(f"Prompt (first 100 chars): {interaction['prompt'][:100]}...")
        print(f"Response (first 100 chars): {interaction['response'][:100]}...")

if __name__ == "__main__":
    asyncio.run(test_workflow())
