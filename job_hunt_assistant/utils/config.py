import os
from dotenv import load_dotenv

load_dotenv()

USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
GEMENI_API_KEY = os.getenv("GEMENI_API_KEY")

