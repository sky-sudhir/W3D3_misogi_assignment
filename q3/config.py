import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Adaptive Prompt Optimizer application."""
    
    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8080))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Application Configuration
    APP_NAME = "Adaptive Prompt Optimizer"
    APP_VERSION = "1.0.0"
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present."""
        if cls.GEMINI_API_KEY == 'your-api-key-here':
            print("WARNING: GEMINI_API_KEY not set. Please set your Gemini API key.")
            print("Get your API key from: https://makersuite.google.com/app/apikey")
            print("Set it as an environment variable: GEMINI_API_KEY=your_key_here")
            return False
        return True 