FROM python:slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY .env .env
CMD ["pytest", "tests/integration/test_character_api.py", "--alluredir=allure-results"]
