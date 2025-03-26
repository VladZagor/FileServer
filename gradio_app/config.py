import os
from pathlib import Path

# Server configuration
SERVER_HOST = "0.0.0.0"  # Listen on all interfaces
SERVER_PORT = 7860  # Default Gradio port

# File storage configuration
STORAGE_DIR = Path("E:\\temp")

# Create storage directory if it doesn't exist
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
