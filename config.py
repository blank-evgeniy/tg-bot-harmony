import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")