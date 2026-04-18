# Credit Risk AI Backend

AI-powered credit risk scoring and lending decision support system built with FastAPI, LangGraph, and Groq LLM.

## 📋 Overview

This backend handles:
- **ML Credit Risk Prediction** - Predicts borrower risk level using trained model
- **Multi-Agent AI Workflow** - Uses LangGraph to orchestrate 5 agents
- **Real Data Processing** - Calculates FOIR, DTI, EMI with actual borrower data
- **Policy Enforcement** - Checks RBI & SBI lending policies
- **LLM Decision Making** - Groq API generates explanations and recommendations

## 🏗️ Architecture

```
API Request (Borrower Form Data)
    ↓
🔄 LangGraph Workflow (5 nodes):
    1. Input Processing (calculate metrics)
    2. ML Prediction (risk score)
    3. Risk Analysis Agent (LLM explains risks)
    4. Policy Retrieval (check rules)
    5. Lending Decision Agent (LLM recommends action)
    ↓
JSON Response (Complete Assessment)
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── core/
│   │   └── config.py           # Settings management
│   ├── graph/
│   │   ├── state.py            # LangGraph state definition
│   │   └── workflow.py         # Multi-agent workflow
│   ├── routes/
│   │   ├── health.py           # Health check endpoints
│   │   └── predict.py          # Main prediction endpoint
│   ├── schemas/
│   │   ├── borrower.py         # Input validation
│   │   └── response.py         # Output models
│   ├── services/
│   │   ├── ml_service.py       # ML model loading & prediction
│   │   ├── groq_service.py     # Groq LLM + AI agents
│   │   └── rag_service.py      # (Coming) Policy retrieval
│   └── utils/
│       ├── helpers.py          # (Coming) Utility functions
│       └── logger.py           # (Coming) Logging setup
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Environment

Create/update `.env` file:

```bash
# Get free API keys from:
# - Groq: https://console.groq.com/keys
# - Qdrant: https://cloud.qdrant.io/

GROQ_API_KEY=your_key_here
DEBUG=True
```

### 3. Run Backend

```bash
# From backend directory
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

### 4. View API Documentation

Visit: `http://localhost:8000/docs`

## 📝 API Endpoints

### Health Check
```
GET /api/health
```
Simple health check.

### Main Prediction
```
POST /api/predict/risk
```

**Input:**
```json
{
  "full_name": "Rajesh Kumar",
  "age": 35,
  "monthly_income": 50000,
  "employment_type": "Salaried",
  "credit_score": 720,
  "existing_loan_amount": 200000,
  "existing_emi_monthly": 5000,
  "loan_amount_requested": 500000,
  "loan_purpose": "Home",
  "loan_tenure_months": 120
}
```

**Output:**
```json
{
  "borrower_name": "Rajesh Kumar",
  "request_id": "REQ_20240418_120530_abc123de",
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
      "Good income level"
    ],
    "confidence_score": 0.82
  },
  "policy_retrieval": {
    "rules_checked": 3,
    "policies_matched": [
      {
        "rule_name": "FOIR Threshold Rule",
        "rule_text": "Monthly EMI should not exceed 45% of monthly income",
        "status": "Violated"
      }
    ]
  },
  "lending_decision": {
    "recommendation": "Manual Review",
    "primary_reason": "FOIR exceeds policy threshold",
    "secondary_reasons": ["Income verification needed"],
    "suggested_action": "Request additional income documents",
    "manual_review_needed": true
  },
  "foir": 0.48,
  "dti": 0.15,
  "proposed_emi": 8000
}
```

## 🔧 Key Calculations

### FOIR (Fixed Obligation to Income Ratio)
```
FOIR = (Existing EMI + Proposed EMI) / Monthly Income
Banks prefer: FOIR < 45%
```

### DTI (Debt-to-Income Ratio)
```
DTI = (Existing Loans + Requested Loan) / Monthly Income
Banks prefer: DTI < 40%
```

### Proposed EMI (Equated Monthly Installment)
```
EMI = P × [r(1+r)^n] / [(1+r)^n - 1]
Where:
  P = Principal (loan amount)
  r = Monthly interest rate (annual rate / 12)
  n = Tenure in months
```

## 🤖 AI Agents

### 1. Risk Analysis Agent
- **Input:** Borrower profile + ML risk score
- **Uses:** Groq LLM
- **Output:** Explains top risk factors and positive factors
- **Example:** "High EMI burden relative to income", "Strong credit score"

### 2. Lending Decision Agent
- **Input:** Risk analysis + policy violations
- **Uses:** Groq LLM
- **Output:** Approve/Reject/Manual Review recommendation with reasoning
- **Example:** "Manual Review - FOIR exceeds 45% threshold"

## 📊 Supported Features

✅ ML-based risk prediction  
✅ Real financial metric calculations  
✅ LangGraph multi-agent workflow  
✅ Groq LLM integration  
✅ Policy rule checking  
✅ Transparent decision reasoning  
✅ API documentation (Swagger)  
✅ Error handling with fallbacks  

## 🔜 Coming Soon

- RAG-based policy retrieval from Qdrant
- PDF report generation
- Request caching
- Rate limiting
- Advanced logging

## 🌐 Development Without API Keys

The backend has **mock fallbacks** for development:

- **Without Groq API Key:** Uses pre-defined risk analysis templates
- **Without ML Model:** Uses rule-based mock predictions
- **Without Qdrant:** Uses basic policy rules instead of RAG

This allows full testing without external services.

## 📚 Tech Stack

| Component | Tech |
|-----------|------|
| Web Framework | FastAPI |
| Server | Uvicorn |
| Validation | Pydantic |
| Multi-Agent | LangGraph |
| LLM | Groq (Mixtral 8x7b) |
| ML Predictions | scikit-learn |
| Vector DB | Qdrant (optional) |

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
Run from `backend/` directory:
```bash
cd backend
uvicorn app.main:app --reload
```

### "Groq API error"
- Check GROQ_API_KEY in .env is valid
- Get free key: https://console.groq.com/keys
- Backend will use mocks if key is invalid

### "Model not found"
- Backend uses mock predictions if .pkl not found
- Place trained model at `./models/credit_risk_model.pkl`

## 📧 Contact & Support

For issues or questions, check the project README.

---

**Happy lending! 🏦**
