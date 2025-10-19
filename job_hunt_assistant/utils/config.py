import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_llm(model='gemini/gemini-2.0-flash', temperature=0.2):
    return LLM(model=model, temperature=temperature, api_key=GEMINI_API_KEY)