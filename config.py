# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access the environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")