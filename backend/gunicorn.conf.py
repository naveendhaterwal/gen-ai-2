import os

# Render sets the PORT environment variable.
# We force gunicorn to bind to this port to ensure the port-scan succeeds.
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Performance tuning (can be overridden by command line flags)
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = 4
timeout = 120
keepalive = 5
