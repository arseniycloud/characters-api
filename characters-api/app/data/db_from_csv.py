import csv

import requests

# Путь к CSV файлу
file_path = 'characters.csv'

# URL API
url = 'http://localhost:8000/character'

# Читаем данные из CSV и делаем POST запросы
with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        character_data = {
            'name': row.get('name'),
            'education': row.get('education'),
            'height': row.get('height'),
            'identity': row.get('identity'),
            'other_aliases': row.get('other_aliases'),
            'universe': row.get('universe'),
            'weight': row.get('weight')
        }

        response = requests.post(url, json=character_data)

        if response.status_code == 200:
            print(f"Персонаж {character_data['name']} успешно добавлен.")
        else:
            print(f"Ошибка при добавлении персонажа {character_data['name']}: {response.json()}")

print("Все персонажи обработаны!")
