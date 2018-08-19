import os
import urllib.parse
from dotenv import load_dotenv
load_dotenv()

# From Heroku config
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

# Separate url parts of REDIS_URL
urllib.parse.uses_netloc.append('redis')
url = urllib.parse.urlparse(REDIS_URL)
REDIS_HOST = url.hostname
REDIS_PORT = url.port
REDIS_PASSWORD = url.password

# Note: heroku sets DATABASE_URl, testing.postgresql sets SQLALCHEMY_DATABASE_URI
# Docker config is set to modify DATABASE_URL
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql://localhost:5432")
# From local env
PRODUCTION = int(os.getenv("PRODUCTION", 0))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_PORT = int(os.getenv("TELEGRAM_PORT") or 8443)
TELEGRAM_DOMAIN = os.getenv("TELEGRAM_DOMAIN")
