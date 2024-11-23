import json
import logging

from colorama import init, Fore, Style

init(autoreset=True)

console_handler = logging.StreamHandler()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

console_handler.setFormatter(logging.Formatter('%(message)s'))


def log_request_response(response):
    request = response.request

    curl_command = f"{Fore.MAGENTA}curl -X {request.method} '{request.url}'"

    for header, value in request.headers.items():
        curl_command += f" -H '{header}: {value}'"
    if request.body:
        curl_command += f" -d '{request.body}'"

    elapsed_time = response.elapsed.total_seconds()

    logger.info(f"Request Curl: {curl_command}\n")

    logger.info(f"Request Method: {request.method}")
    logger.info(f"Request URL: {Fore.GREEN}{request.url}{Style.RESET_ALL}")
    logger.info(f"Request Headers: {request.headers}")

    if request.body:
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            formatted_request_json = json.dumps(request_json, indent=4)
            logger.info(f"Request Json: {formatted_request_json}")
        except (ValueError, AttributeError):
            logger.info(f"Request Json: {request.body}")

    status_color = Fore.GREEN if response.status_code == 200 else Fore.YELLOW
    logger.info(f"Response Status Code: {status_color}{response.status_code}{Style.RESET_ALL}")

    try:
        response_json = json.dumps(response.json(), indent=4)
    except ValueError:
        response_json = response.text

    logger.info(f"Response Json: {response_json}")

    logger.info(f"Response Time: {Fore.BLUE}{round(elapsed_time, 3)}{Style.RESET_ALL} seconds\n")
