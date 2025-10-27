import csv

import requests

# Path to CSV file
file_path = 'characters.csv'

# API URL
url = 'http://localhost:8000/character'

# Read data from CSV and make POST requests
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
            print(f"Character {character_data['name']} successfully added.")
        else:
            print(f"Error adding character {character_data['name']}: {response.json()}")

print("All characters processed!")
