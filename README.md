# credit-risk-ai

AI-powered Credit Risk & Lending Decision Support System.

## Project Structure

- `frontend/` - Next.js app for the borrower form, dashboard, and result pages.
- `backend/` - FastAPI app for prediction, RAG, Groq, and report generation.
- `docs/` - RBI and SBI policy documents used by the retrieval layer.
- `shared/` - Optional shared schemas or sample JSON payloads.

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- A Groq API key
- Qdrant Cloud credentials

## Install

### 1) Frontend

```bash
cd "/Users/n2/Desktop/gen ai project /credit-risk-ai/frontend"
npm install
```

### 2) Backend

```bash
cd "/Users/n2/Desktop/gen ai project /credit-risk-ai/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Create `backend/.env` and add the values below:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=credit_risk_docs
MODEL_PATH=app/models/loan_model.pkl
PREPROCESSOR_PATH=app/models/preprocessor.pkl
RBI_DOC_PATH=../docs/RBI_Guidelines_Summary.txt
SBI_DOC_PATH=../docs/SBI_Internal_Loan_Policy.txt
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=info
```

## Run the Project

### Terminal 1 - Backend

```bash
cd "/Users/n2/Desktop/gen ai project /credit-risk-ai/backend"
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend

```bash
cd "/Users/n2/Desktop/gen ai project /credit-risk-ai/frontend"
npm run dev
```

## Access URLs

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

## Build Priority

1. Backend schema, prediction route, and health route.
2. Frontend borrower form and API client.
3. RAG workflow for RBI and SBI document retrieval.
4. Recommendation and report generation.
5. Dashboard charts and PDF export.

## Deployment Notes

- Deploy frontend on Vercel.
- Deploy backend on Render.
- Keep all secrets in environment variables, not in source control.
- Upload the two policy documents in `docs/` before enabling RAG.