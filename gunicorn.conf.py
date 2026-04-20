import os
import sys

# Add backend directory to sys.path so we can import app.main
sys.path.append(os.path.join(os.getcwd(), "backend"))

# Render sets the PORT environment variable.
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Worker configuration
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
accesslog = "-"
errorlog = "-"
