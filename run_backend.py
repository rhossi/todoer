#!/usr/bin/env python3
"""Run the FastAPI backend server"""
import sys
import os

# Check if we're using the venv's Python (handle both python and python3)
project_root = os.path.dirname(__file__)
venv_python = os.path.join(project_root, ".venv", "bin", "python")
venv_python3 = os.path.join(project_root, ".venv", "bin", "python3")
venv_exists = os.path.exists(venv_python) or os.path.exists(venv_python3)

# Check if sys.executable is in the venv (works for both python and python3)
if venv_exists and ".venv" not in sys.executable:
    print(f"Warning: Using {sys.executable} instead of venv Python", flush=True)
    print(f"Please run: uv run python run_backend.py", flush=True)

print("Starting FastAPI backend server...", flush=True)
print("Loading application...", flush=True)

try:
    import uvicorn
except ImportError:
    print("ERROR: uvicorn is not installed!", flush=True)
    print("Please install dependencies with: uv sync", flush=True)
    print("Or run with: uv run python run_backend.py", flush=True)
    sys.exit(1)

if __name__ == "__main__":

    # Configure uvicorn with explicit logging
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Only watch specific directories (exclude .venv, frontend, etc.)
    # Use absolute paths to ensure uvicorn watches only these directories
    reload_dirs = [
        os.path.join(project_root, "backend"),
        os.path.join(project_root, "agent"),
        os.path.join(project_root, "mcp_server"),
    ]
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=reload_dirs,
        log_level="info",
        access_log=True
    )

