import os

from dotenv import load_dotenv

load_dotenv()

# Define base URL based on environment
ENVIRONMENT = os.getenv('ENV')
API_URLS = {
    'dev': 'http://dev.test.ivi.ru/v2',
    'prod': 'http://rest.test.ivi.ru/v2'
}

API_BASE_URL = API_URLS.get(ENVIRONMENT)

if not API_BASE_URL:
    raise ValueError("API_BASE_URL is not set and has no default value.")

USERNAME = os.getenv('API_USERNAME')
PASSWORD = os.getenv('API_PASSWORD')
