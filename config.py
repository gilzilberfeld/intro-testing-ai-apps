import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Test configuration
TEST_TIMEOUT = 30
MAX_RETRIES = 3