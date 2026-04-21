# Credit Risk AI — Multi-Agent Assessmennt System

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/AI-LangGraph-blue?style=flat-square)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203-orange?style=flat-square)](https://groq.com/)
[![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant%20Cloud-red?style=flat-square)](https://qdrant.tech/)
[![Vercel](https://img.shields.io/badge/Deployed-Vercel-black?style=flat-square&logo=vercel)](https://gen-ai-2.vercel.app)

> An enterprise-grade credit risk assessment platform that combines **Machine Learning**, **Retrieval-Augmented Generation (RAG)**, and **Multi-Agent Orchestration** to deliver high-fidelity, real-time lending decisions — now with an **interactive AI chatbot** powered by Groq.

---


##  Key Features

| Feature | Description |
|---|---|
| **Hybrid Risk Scoring** | Blends a Logistic Regression ML model (40%) with a deterministic Banking Rule Engine (60%) for sensitive and reliable scoring |
| **Multi-Agent Workflow** | Powered by **LangGraph**, orchestrating specialized agents for Risk Analysis, Policy Retrieval, and Final Lending Decisions |
| **RAG Policy Compliance** | Uses **Qdrant Cloud** for semantic search across RBI/SBI banking policies to ensure regulatory compliance |
| **🆕 AI Chat Sidebar** | Interactive `ChatAgent` powered by **Groq LLM** — ask natural language questions about any loan report in real time |
| **Real-Time Traceability** | Full step-by-step execution trace with detailed input/output logs and model transparency |
| **Premium UI/UX** | Responsive dark-mode dashboard with glassmorphism, Framer Motion animations, and a clean two-column layout |

---

##  Technology Stack

### Frontend
- **Next.js 14** (App Router)
- **Tailwind CSS** — utility-first styling
- **Framer Motion** — animations & micro-interactions
- **Recharts** — financial data visualization
- **Lucide Icons** — icon set

### Backend
- **FastAPI** (Python 3.11+)
- **LangGraph** — multi-agent orchestration
- **Pydantic v2** — data validation
- **Uvicorn + Gunicorn** — production ASGI server

### Intelligence Layer
- **Groq Cloud** (`llama-3.1-8b-instant`) — LLM for risk analysis, lending decisions, and AI chat
- **Qdrant Cloud** — vector storage for RAG-based policy retrieval
- **Scikit-Learn** — ML model for risk scoring

### Deployment
- **Frontend**: [Vercel](https://gen-ai-2.vercel.app)
- **Backend**: [Render](https://gen-ai-2-o6m1.onrender.com)

---

## 🆕 AI Chat Sidebar

The interactive **AI Response Sidebar** allows users to ask natural language questions directly about any generated credit risk report.

- **Powered by**: Groq Llama 3.1
- **Context-aware**: Sends only essential, filtered report data (risk analysis, decision, FOIR/DTI, policy matches) to stay within token limits
- **Endpoint**: `POST /api/report/{request_id}/chat`
- **Quick Ask prompts** for common queries (e.g., *"Why is this applicant risky?"*)
- Clean, minimal chat bubble UI with Claude-style bouncing-dot loading animation

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Groq API Key](https://console.groq.com/keys)
- [Qdrant Cloud Account](https://cloud.qdrant.io/)

---

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

Optionally create `.env.local` inside `frontend/`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

### 3. Running Locally

**Terminal 1 — Backend:**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Visit **[http://localhost:3000](http://localhost:3000)** to begin a new credit assessment.

> **Note:** Reports are cached in-memory. If you restart the backend, submit a new assessment to generate a fresh report ID.

---

## 📂 Repository Structure

```
credit-risk-ai/
├── backend/
│   ├── app/
│   │   ├── graph/          # LangGraph multi-agent workflow
│   │   ├── routes/         # FastAPI route handlers (predict, report, chat)
│   │   ├── services/       # Groq LLM, ML model, RAG, ChatAgent
│   │   └── main.py
│   ├── models/             # Serialized ML model & feature config
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   └── results/[id]/   # Dynamic results page
│   ├── components/
│   │   ├── AIPolicySidebar.tsx   # AI Chat Sidebar component
│   │   ├── ResultsDashboard.tsx  # Main insight dashboard
│   │   └── WorkflowTrace.tsx     # Agent execution trace
│   └── lib/
│       └── api.ts          # API client (including chatWithReport)
├── docs/                   # Banking policy PDFs for RAG seeding
└── README.md
```

---

##  License

Distributed under the MIT License. See `LICENSE` for more information.
