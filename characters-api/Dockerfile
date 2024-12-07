# Используем Python image
FROM python:3.12
# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем файлы приложения
COPY . /app
# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
# Добавляем команду для запуска скрипта импорта и затем приложения
CMD ["bash", "-c", "python app/data/db_from_csv.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
