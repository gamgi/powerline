import os
from dotenv import load_dotenv
load_dotenv()

PRODUCTION = int(os.getenv("PRODUCTION") or 0)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_PORT = int(os.getenv("TELEGRAM_PORT") or 8443)
TELEGRAM_DOMAIN = os.getenv("TELEGRAM_DOMAIN")
