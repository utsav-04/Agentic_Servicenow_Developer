import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ServiceNow
INSTANCE = os.getenv("SERVICENOW_INSTANCE")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")