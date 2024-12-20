from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access the API key like this
api_key = os.getenv('ANTHROPIC_API_KEY') 