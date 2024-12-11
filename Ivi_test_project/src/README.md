## Структура

    ├── README.md
    ├── __init__.py
    ├── api_client.py
    ├── character_data.py
    ├── characters_cleaner.py
    ├── logger.py
    ├── models.py
    ├── schemas.py
    └── utils
        ├── __init__.py
        └── create_random_character.py

1. api_client.py: - Модуль для взаимодействия с API, включает методы для отправки запросов и получения
   данных.
2. character_data.py: - Содержит функции и классы для работы с данными персонажей.
3. characters_cleaner.py: - Скрипт для поиска и удаления персонажей на основе различных критериев.
4. logger.py: - Настройка и использование системы логирования для отслеживания работы скриптов.
5. models.py: - Определение моделей данных, используемых в проекте.
6. schemas.py: - Содержит схемы для валидации и сериализации данных.
7. utils/: - Директория, содержащая вспомогательные утилиты



### Чистка персонажей
![Test Project](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGxzOXVraGl4cGp3cXNoNTVkd2RpZXpuank5eXU3dWFtN3ozZzB6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0HlzA7eron1msyhW/giphy.gif)  <!-- Замените ссылку на подходящую GIF-картинку -->

## Использование characters_cleaner.py

Используйте characters_cleaner.py для поиска и удаления персонажей из базы данных:

Search characters by height:

    python character_cleanup.py --search --height 175

Search characters by education:

    python characters_cleaner.py --search --education "High school, university level courses in languages & computer science"

Search characters by multiple criteria

    python character_cleanup.py --search --education "High school, university level courses in languages & 
    computer science" --height 175 --identity "Secret" --other_aliases "None" --universe "Marvel Universe" 
    --weight 67.5


Delete characters by education:

    python character_cleanup.py --delete --education "High school, university level courses in languages & computer science"

Delete characters by height:
    
    python character_cleanup.py --delete --height 175

Delete characters with limit flag

    python src/character_cleanup.py --delete --limit 10


Delete characters by multiple criteria:
   
    python character_cleanup.py --delete --education "High school, university level courses in languages &
    computer science" --height 175 --identity "Secret" --other_aliases "None" --universe "Marvel Universe"
    --weight 67.5
   
