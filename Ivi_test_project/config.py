import os

from dotenv import load_dotenv

load_dotenv()

# Определение базового URL в зависимости от среды
ENVIRONMENT = os.getenv('ENV')
API_URLS = {
    'dev': 'http://dev.test.ivi.ru/v2',
    'prod': 'http://rest.test.ivi.ru/v2'
}
    
API_BASE_URL = API_URLS.get(ENVIRONMENT)

if not API_BASE_URL:
    raise ValueError("API_BASE_URL не задано и не имеет значения по умолчанию.")

USERNAME = os.getenv('API_USERNAME')
PASSWORD = os.getenv('API_PASSWORD')
