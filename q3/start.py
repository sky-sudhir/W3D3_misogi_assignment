"""
Simple startup script for the Adaptive Prompt Optimizer
This script helps debug loading issues with the FastAPI application
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set default API key for testing if not provided
if not os.getenv('GEMINI_API_KEY'):
    print("WARNING: No GEMINI_API_KEY found in environment. Using test key.")
    os.environ['GEMINI_API_KEY'] = 'test-key-for-debugging'

def main():
    print("=" * 60)
    print("Starting Adaptive Prompt Optimizer in DEBUG mode")
    print("=" * 60)
    
    # Configure uvicorn server with debug settings
    config = uvicorn.Config(
        "app:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        reload_dirs=[".", "templates", "static"],
        log_level="debug",
    )
    
    # Start the server
    server = uvicorn.Server(config)
    print("Server configured. Starting...")
    server.run()

if __name__ == "__main__":
    main() 