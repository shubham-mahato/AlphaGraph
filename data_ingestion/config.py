import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
  raise ValueError("NEWS_API_KEY not found in .env file!")

NEWS_SOURCE =[
  "reuters",
  "bloomberg",
  "cnbc",
  "financial-times",
  "the-times-of-india",
  "business-standard"
]

COMPANY_KEYWORDS = [
    "Tata Consultancy Services",
    "Infosys",
    "HDFC Bank",
    "ICICI Bank",
    "Reliance Industries"
]
