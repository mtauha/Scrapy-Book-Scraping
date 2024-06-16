import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file if present

DATABASE_URL = os.getenv("DATABASE-URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")
