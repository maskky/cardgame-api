import os

from dotenv import load_dotenv

# dotenv doesn't override existing environment from docker-compose.yml
load_dotenv(".env")

MONGODB_URL = os.environ.get('MONGODB_URL')
TOTAL_CARD = int(os.environ.get('TOTAL_CARD'))
SECRET_KEY = os.environ.get('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))