from dotenv import load_dotenv
import os

# Load .env file into environment
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# App settings
APP_NAME = "CodeFlow AI"
APP_VERSION = "1.0.0"
FRONTEND_URL = "http://localhost:3000"