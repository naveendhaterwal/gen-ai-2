# 🚀 Deployment Guide

This guide covers how to deploy the **Credit Risk AI** platform for free using Vercel (Frontend) and Render (Backend).

## 1. Prerequisites
- Accounts on [GitHub](https://github.com), [Vercel](https://vercel.com), and [Render](https://render.com).
- Your code must be pushed to a GitHub repository.

---

## 2. GitHub Sync (The Hand-off)
Since I cannot push to your GitHub directly due to security, please run these commands in your local terminal:

```bash
git add .
git commit -m "chore: prepare for production deployment"
git push origin your-branch-name
```
*If you get an authentication error, use a [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).*

---

## 3. Backend Deployment (Render)
1. Log in to [Render](https://dashboard.render.com).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. Set the following:
   - **Name**: `credit-risk-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
5. **Environment Variables**: Add the following:
   - `GROQ_API_KEY`: *(Your Key)*
   - `QDRANT_URL`: *(Your Qdrant Cluster URL)*
   - `QDRANT_API_KEY`: *(Your Qdrant API Key)*
   - `STRICT_NO_FALLBACKS`: `True`
   - `CORS_ORIGINS`: `https://your-frontend-url.vercel.app` *(Update this after deploying frontend)*

---

## 4. Frontend Deployment (Vercel)
1. Log in to [Vercel](https://vercel.com).
2. Click **Add New** > **Project**.
3. Import your GitHub repository.
4. Configure the Project:
   - **Project Name**: `credit-risk-frontend`
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`
5. **Environment Variables**: Add:
   - `NEXT_PUBLIC_API_URL`: `https://your-backend-url.onrender.com` *(Copy this from your Render dashboard)*
6. Click **Deploy**.

---

## 5. Final Connection
Once both are deployed:
1. Copy your Vercel URL (e.g., `https://credit-risk-frontend.vercel.app`).
2. Go back to Render > Environment Variables.
3. Update `CORS_ORIGINS` with your Vercel URL.
4. Render will automatically redeploy.

---

