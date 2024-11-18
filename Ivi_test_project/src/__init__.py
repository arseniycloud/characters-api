import os

from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Убедитесь, что переменные загружены
assert os.getenv('API_USERNAME') is not None, "API_USERNAME not set in environment"
assert os.getenv('API_PASSWORD') is not None, "API_PASSWORD not set in environment"
