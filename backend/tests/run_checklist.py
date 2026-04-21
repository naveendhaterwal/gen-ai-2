
from fastapi.testclient import TestClient

from app.main import app
from app.services.groq_service import groq_service
from app.services.rag_service import rag_service
from app.services.ml_service import ml_service

results = []


def record(name: str, ok: bool, detail: str) -> None:
    results.append((name, "PASS" if ok else "FAIL", detail))


client = TestClient(app)

# 1. Environment/dependency readiness
record("ML model loaded", bool(ml_service.model_loaded), f"model_loaded={ml_service.model_loaded}")
record("Groq client configured", bool(groq_service.client), f"groq_client={bool(groq_service.client)}")
q_health = rag_service.health_status()
record("Qdrant health ready", bool(q_health.get("ready")), str(q_health))

# 2. Health endpoints
h1 = client.get("/health")
record("GET /health", h1.status_code == 200, f"status={h1.status_code}")

h2 = client.get("/api/health/")
record("GET /api/health/", h2.status_code == 200, f"status={h2.status_code}")

h3 = client.get("/api/health/detailed")
record(
    "GET /api/health/detailed",
    h3.status_code == 200,
    f"status={h3.status_code}, body={h3.json() if h3.status_code == 200 else ''}",
)

h4 = client.get("/api/health/ready")
record("GET /api/health/ready", h4.status_code == 200, f"status={h4.status_code}")

h5 = client.get("/api/health/version")
record("GET /api/health/version", h5.status_code == 200, f"status={h5.status_code}")

# 3. Prediction happy path
payload = {
    "full_name": "Rajesh Kumar",
    "age": 35,
    "monthly_income": 50000,
    "employment_type": "Salaried",
    "credit_score": 720,
    "existing_loan_amount": 200000,
    "existing_emi_monthly": 5000,
    "loan_amount_requested": 500000,
    "loan_purpose": "Home",
    "loan_tenure_months": 120,
}

pred = client.post("/api/predict/risk", json=payload)
record("POST /api/predict/risk happy path", pred.status_code == 200, f"status={pred.status_code}")

request_id = None
if pred.status_code == 200:
    data = pred.json()
    request_id = data.get("request_id")
    has_fields = all(
        key in data
        for key in [
            "risk_analysis",
            "policy_retrieval",
            "lending_decision",
            "foir",
            "dti",
            "proposed_emi",
        ]
    )
    record("Predict response contract", has_fields, f"request_id={request_id}, keys_ok={has_fields}")

    policy_matches = data.get("policy_retrieval", {}).get("policies_matched", [])
    policy_sources = sorted(
        set(item.get("source", "unknown") for item in policy_matches if isinstance(item, dict))
    )
    record("Policy source is qdrant", "qdrant" in policy_sources, f"policy_sources={policy_sources}")

# 4. Validation error test
bad_payload = dict(payload)
bad_payload["age"] = 15
bad = client.post("/api/predict/risk", json=bad_payload)
record("POST /api/predict/risk invalid age -> 422", bad.status_code == 422, f"status={bad.status_code}")

# 5. Report endpoints
rep = client.post("/api/report/generate", json=payload)
record("POST /api/report/generate", rep.status_code == 200, f"status={rep.status_code}")

rep_alias = client.post("/api/report/generate-report", json=payload)
record("POST /api/report/generate-report", rep_alias.status_code == 200, f"status={rep_alias.status_code}")

if request_id:
    get_rep = client.get(f"/api/report/{request_id}")
    record("GET /api/report/{request_id}", get_rep.status_code == 200, f"status={get_rep.status_code}")

missing_rep = client.get("/api/report/REQ_DOES_NOT_EXIST")
record("GET /api/report/{missing} -> 404", missing_rep.status_code == 404, f"status={missing_rep.status_code}")

# 6. Groq direct live probe
try:
    llm_out = groq_service.call_llm(
        '{"task":"ping"}',
        system_prompt="Return strict JSON only.",
        temperature=0,
        max_tokens=20,
    )
    record("Groq live API call", True, f"response={str(llm_out)[:120]}")
except Exception as exc:
    record("Groq live API call", False, f"error={exc}")

# 7. Qdrant direct retrieval probe
try:
    retrieval = rag_service.retrieve_policies(
        {
            "age": 35,
            "monthly_income": 50000,
            "employment_type": "Salaried",
            "credit_score": 720,
            "loan_amount_requested": 500000,
            "loan_purpose": "Home",
            "foir": 0.42,
            "dti": 0.31,
        }
    )
    source = retrieval.get("source")
    count = len(retrieval.get("policies", []))
    warnings = retrieval.get("warnings", [])
    record(
        "Qdrant retrieval live source",
        source == "qdrant",
        f"source={source}, count={count}, warnings={warnings}",
    )
except Exception as exc:
    record("Qdrant retrieval live source", False, f"error={exc}")

print("\n=== BACKEND TEST REPORT ===")
passed = 0
for name, status, detail in results:
    print(f"[{status}] {name}: {detail}")
    if status == "PASS":
        passed += 1

print(f"\nSummary: {passed}/{len(results)} passed")
