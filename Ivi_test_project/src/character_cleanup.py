import argparse
import logging
import requests
from requests.auth import HTTPBasicAuth
import json  # добавляем импорт модуля json для форматирования вывода

# Конфигурация API
API_BASE_URL = "http://rest.test.ivi.ru/v2"
API_USERNAME = "arseniypolyakov1@gmail.com"
API_PASSWORD = "APZrVp83vFNk5F"

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_all_characters():
    """ Получает всех персонажей из API и возвращает список. """
    session = requests.Session()
    session.auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)
    try:
        logger.info(f"Отправка запроса: GET {API_BASE_URL}/characters")
        response = session.get(f"{API_BASE_URL}/characters")
        response.raise_for_status()
        data = response.json()
        logger.info("Данные успешно получены.")
        return data.get("result", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при выполнении запроса: {e}")
        return []
    except ValueError as e:
        logger.error(f"Ошибка преобразования JSON: {e}")
        return []

def filter_characters_by_criteria(characters, **criteria):
    """ Возвращает список имен персонажей, соответствующих критериям. """
    matched_characters = []
    for character in characters:
        if all((criteria[key] is None or character.get(key) == criteria[key]) for key in criteria):
            matched_characters.append(character)  # сохраняем весь объект для вывода всех данных
            logger.info(f"Найден персонаж: {character.get('name')}")
            # выводим JSON параметры персонажа
            logger.info(f"Информация о персонаже: {json.dumps(character, ensure_ascii=False, indent=4)}")
    return matched_characters

def delete_characters_by_name(character_names, limit=None):
    """ Удаляет персонажей по именам до указанного лимита. """
    session = requests.Session()
    session.auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)
    deletion_count = 0

    for character in character_names:
        name = character.get('name')
        if limit is not None and deletion_count >= limit:
            break
        try:
            logger.info(f"Удаление персонажа: {name}")
            response = session.delete(f"{API_BASE_URL}/character", params={'name': name})
            response.raise_for_status()
            deletion_count += 1
            logger.info(f"Персонаж {name} успешно удален.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при удалении {name}: {e}")

    logger.info(f"Удалено всего {deletion_count} персонажей.")

def main(perform_search=False, perform_deletion=False, limit=None, **criteria):
    """ Основная логика скрипта: поиск и удаление персонажей по критериям. """
    all_characters = get_all_characters()
    matched_characters = filter_characters_by_criteria(all_characters, **criteria)

    if perform_search:
        total_count = len(matched_characters)
        if total_count > 0:
            logger.info(f"Найдено {total_count} подходящих персонажей.")
        else:
            logger.info("Нет подходящих персонажей.")

    if perform_deletion:
        delete_characters_by_name(matched_characters, limit=limit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Поиск и удаление персонажей по критериям.')
    parser.add_argument('--search', action='store_true', help='Искать персонажей.')
    parser.add_argument('--delete', action='store_true', help='Удалить персонажей.')
    parser.add_argument('--limit', type=int, default=None, help='Лимит на количество удаляемых персонажей.')
    parser.add_argument('--education', type=str, help='Критерий образования.')
    parser.add_argument('--height', type=int, help='Критерий роста.')
    parser.add_argument('--identity', type=str, help='Критерий идентичности.')
    parser.add_argument('--other_aliases', type=str, help='Критерий других имён.')
    parser.add_argument('--universe', type=str, help='Критерий вселенной.')
    parser.add_argument('--weight', type=float, help='Критерий веса.')
    args = parser.parse_args()

    main(
        perform_search=args.search,
        perform_deletion=args.delete,
        limit=args.limit,
        education=args.education,
        height=args.height,
        identity=args.identity,
        other_aliases=args.other_aliases,
        universe=args.universe,
        weight=args.weight
    )
