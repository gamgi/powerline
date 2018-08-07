import os
from dotenv import load_dotenv
load_dotenv()

PRODUCTION = int(os.getenv("PRODUCTION"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_PORT = os.getenv("TELEGRAM_PORT")
TELEGRAM_DOMAIN = os.getenv("TELEGRAM_DOMAIN")
