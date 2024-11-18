import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_request_response(response):
    request = response.request

    # Формируем команду curl для запроса
    curl_command = f"curl -X {request.method} '{request.url}'"

    # Добавляем заголовки
    for header, value in request.headers.items():
        curl_command += f" -H '{header}: {value}'"

    # Добавляем данные запроса, если они есть
    if request.body:
        curl_command += f" -d '{request.body}'"

    # Вычисляем время ответа
    elapsed_time = response.elapsed.total_seconds()

    # Логируем команду curl
    logger.info(f"Request Curl: {curl_command}")

    # Логируем данные запроса и ответа
    logger.info(f"Request Method: {request.method}")
    logger.info(f"Request URL: {request.url}")
    logger.info(f"Request Headers: {request.headers}")
    logger.info(f"Request Json: {request.body}")

    # Логирование ответа с временем
    logger.info(f"Response Status Code: {response.status_code}")
    logger.info(f"Response Json: {response.text}")
    logger.info(f"Response Time: {round(elapsed_time, 3)} seconds")
