#!/usr/bin/env python3
"""
Adaptive Prompt Optimizer Runner
Simple script to start the application with proper checks.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import google.generativeai
        import jinja2
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e.name}")
        print("Run: pip install -r requirements.txt")
        return False

def check_gemini_api_key():
    """Check if Gemini API key is set."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your-api-key-here':
        print("✗ GEMINI_API_KEY not set")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        print("Set it with: set GEMINI_API_KEY=your_key_here (Windows)")
        print("Or: export GEMINI_API_KEY=your_key_here (Linux/Mac)")
        return False
    print("✓ Gemini API key is configured")
    return True

def main():
    """Main function to run checks and start the application."""
    print("🚀 Adaptive Prompt Optimizer - Starting...")
    print("=" * 50)
    
    # Run checks
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_gemini_api_key():
        print("\n⚠️  Warning: API key not set. The application will start but won't work properly.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("=" * 50)
    print("✓ All checks passed! Starting the application...")
    
    # Start the application
    try:
        from app import app
        from config import Config
        import uvicorn
        
        print(f"🌐 Open your browser to: http://localhost:{Config.PORT}")
        uvicorn.run(app, host=Config.HOST, port=Config.PORT, reload=Config.DEBUG)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 