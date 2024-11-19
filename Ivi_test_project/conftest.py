import logging
from http import HTTPStatus

import pytest

from src.api_client import CharacterClient

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="class")
def character_client():
    return CharacterClient()


@pytest.fixture(scope='function')
def characters_to_cleanup(character_client):
    """Фикстура для удаления персонажа после теста"""
    created_characters = []

    yield created_characters

    for name in created_characters:
        try:
            logger.info(f"Попытка удалить персонажа '{name}'...")
            response = character_client.delete_character(name)
            logger.info(f"URL запроса на удаление персонажа: {response.request.url}")
            if response.status_code == HTTPStatus.OK:
                logger.info(f"Персонаж '{name}' успешно удалён.")
            elif response.status_code == HTTPStatus.BAD_REQUEST:
                logger.warning(
                    f"Персонаж '{name}' не найден или не может быть удален. Статус: {response.status_code}")
            else:
                logger.error(f"Неожиданный код статуса при удалении '{name}': {response.status_code}")
        except Exception as e:
            logger.error(f"Ошибка при попытке удалить персонажа '{name}': {str(e)}")
