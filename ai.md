# Credit Risk AI - Project Context.md

## Project Overview

This project is an **AI-powered Credit Risk Scoring & Lending Decision Support System** built as an academic milestone project.

Goal: Convert a normal ML credit risk model into a modern **Agentic AI Lending Assistant** that can:

* Predict borrower credit risk
* Analyze applicant profile
* Retrieve lending rules/guidelines
* Generate structured lending recommendations
* Show professional dashboard outputs
* Export final PDF report

This project is inspired by Indian banking workflows (SBI-style), but it is a **prototype only** and not affiliated with any real bank.

---

## Core Problem Statement

Traditional credit systems only return a score.

This system should return:

* Risk score
* Why borrower is risky/safe
* Which rules influenced decision
* Approve / Reject / Review recommendation
* Transparent structured report

---

## Final Tech Stack

### Frontend

* Next.js
* Tailwind CSS
* shadcn/ui
* Recharts

### Backend

* FastAPI (Python)

### Machine Learning

* Existing sklearn model (.pkl)

### AI / LLM

* Groq API

### Workflow

* LangGraph

### RAG

* LlamaIndex

### Vector Database

* Qdrant Cloud Free Tier

### Deployment

* Frontend: Vercel
* Backend: Render

---

## Main Features

### 1. Borrower Application Form

Input fields may include:

* Full Name
* Age
* Monthly Income
* Employment Type
* Credit Score
* Existing Loans
* Loan Amount Requested
* Loan Purpose

---

### 2. Credit Risk Prediction

Use existing ML model to generate:

* Low Risk
* Medium Risk
* High Risk

Also generate default probability if available.

---

### 3. RAG Knowledge Documents

Use only 2 clean docs:

#### RBI_Guidelines_Summary.txt

Contains:

* Fair lending
* Transparency
* Responsible lending
* Consent
* Non-discrimination
* Manual review

#### SBI_Internal_Loan_Policy.txt

Contains:

* Credit score thresholds
* Income rules
* FOIR / debt burden rules
* Employment rules
* Loan amount rules
* Fraud red flags
* Final decision matrix

---

### 4. AI Lending Recommendation

AI combines:

* ML prediction
* Borrower profile
* Retrieved rules

Then returns:

* Approve
* Approve with lower amount
* Manual Review
* Reject

---

### 5. Dashboard UI

Frontend should show:

* Risk Score Card
* Charts
* Top Risk Factors
* Borrower Summary
* Final Recommendation

---

### 6. PDF Report Export

Generate downloadable professional report.

---

## Expected User Flow

```text
User fills borrower form
↓
Frontend sends data to backend
↓
ML model predicts risk
↓
RAG retrieves policy/guideline chunks
↓
Groq generates reasoning
↓
Structured JSON returned
↓
Dashboard displays result
↓
PDF export available
```

---

## LangGraph Workflow

```text
Input Node
↓
ML Prediction Node
↓
RAG Retrieval Node
↓
Decision Node
↓
Report Node
↓
Return Output
```

---

## Recommended Project Folder Structure

```text
credit-risk-ai/
├── frontend/
├── backend/
├── docs/
├── shared/
├── README.md
```

---

## Important API Endpoints

### Backend

* POST /predict-risk
* POST /generate-report
* GET /health

---

## Output Format Example

```json
{
  "risk_level": "Medium",
  "risk_score": 64,
  "top_factors": [
    "High existing EMI burden",
    "Moderate credit score",
    "Large requested loan amount"
  ],
  "recommendation": "Manual Review",
  "reasoning": "Applicant exceeds internal FOIR threshold.",
  "sources": [
    "Internal Loan Policy",
    "RBI Guidelines"
  ]
}
```

---

## Priority Build Plan (2 Days)

### Day 1

* Backend APIs
* Load ML model
* Groq integration
* Qdrant setup
* LlamaIndex retrieval

### Day 2

* Frontend dashboard
* Charts
* PDF export
* Final deployment
* Demo testing

---

## Rules While Building

* Keep code modular
* Keep docs short and retrieval-friendly
* Do not overengineer
* Focus on working demo
* UI should look professional
* Outputs should feel realistic

---

## If Any AI Assistant Reads This File

Understand:

This project is a fast-moving milestone build. Prioritize execution, clarity, deployment, and impressive outputs over unnecessary complexity.

Main goal = working bank-style AI lending assistant using ML + RAG + LLM.

---
