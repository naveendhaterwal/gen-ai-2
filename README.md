# Credit Risk AI - Multi-Agent Assessment System

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/AI-LangGraph-blue?style=flat-square)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange?style=flat-square)](https://groq.com/)

An enterprise-grade credit risk assessment platform that combines **Machine Learning**, **Retrieval-Augmented Generation (RAG)**, and **Multi-Agent Orchestration** to provide high-fidelity lending decisions.

---

## 🔥 Key Features

- **Hybrid Risk Scoring**: Blends a Logistic Regression ML model (40%) with a deterministic Banking Rule Engine (60%) for sensitive and reliable scoring.
- **Multi-Agent Workflow**: Powered by **LangGraph**, the system orchestrates specialized agents for Risk Analysis, Policy Retrieval, and Final Lending Decisions.
- **Context-Aware Policy Retrieval**: Uses **Qdrant Cloud** to perform lexical and semantic search across banking policies (RBI, SBI, etc.) to ensure compliance.
- **Real-Time Traceability**: Deep visibility into the backend execution with step-by-step input/output logging and model transparency.
- **Premium UI/UX**: Responsive Next.js dashboard featuring glassmorphism and real-time assessment streaming.

---


## 🛠️ Technology Stack

- **Frontend**: Next.js 14, Tailwind CSS, Framer Motion, Lucide Icons.
- **Backend**: FastAPI (Python 3.11+), LangGraph, Pydantic v2.
- **Intelligence**: Groq Llama 3.1 (LLM), Scikit-Learn (ML).
- **Database**: Qdrant Cloud (Vector Database for RAG).

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Groq API Key](https://console.groq.com/keys)
- [Qdrant Cloud Account](https://cloud.qdrant.io/)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_key_here
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
STRICT_NO_FALLBACKS=True
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. Running Locally

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
python app/main.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` to start assessments.

---

## 📂 Repository Structure

- `frontend/`: Next.js application with assessment dashboard.
- `backend/`: FastAPI services, AI agents, and ML pipelines.
- `docs/`: Banking policy documents used for RAG seeding.
- `backend/models/`: Serialized ML model and feature configuration.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
