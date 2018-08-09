import os
from dotenv import load_dotenv
load_dotenv()

# From Heroku config
REDIS_URL = os.getenv("REDIS_URL", "redis:6379")
(REDIS_HOST, REDIS_PORT) = REDIS_URL.rsplit(':', 1)

# From local env
PRODUCTION = int(os.getenv("PRODUCTION", 0))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_PORT = int(os.getenv("TELEGRAM_PORT") or 8443)
TELEGRAM_DOMAIN = os.getenv("TELEGRAM_DOMAIN")
