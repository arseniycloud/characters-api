import random
from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus

import allure
import pytest

from src.character_data import CHARACTER_DATA, MOST_COMMON_CHARACTER_NAMES
from src.schemas import CharacterResponseSchema, CharactersListSchema
from src.utils.create_random_character import create_random_character


@allure.feature('Characters API')
@pytest.mark.character_api
class TestCharactersAPI:

    ### Positive Tests ###

    @allure.story('Positive: Получение всех персонажей')
    def test_get_characters(self, character_client):
        response = character_client.get_characters()
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharactersListSchema)

    @allure.story('Positive: Получение персонажа по имени')
    @pytest.mark.parametrize("character", MOST_COMMON_CHARACTER_NAMES)
    def test_get_character_by_name(self, character_client, character):
        response = character_client.get_character_by_name(character)
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)

    @allure.story('Positive: Добавление персонажа с фейковыми данными')
    def test_add_character_with_faker(self, character_client, characters_to_cleanup):
        random_character = create_random_character()
        response = character_client.add_character(random_character)

        # Проверяем, если персонаж уже существует
        while response.status_code == HTTPStatus.BAD_REQUEST:
            random_character["name"] = random_character["name"][:-2]  # Укорачиваем имя на 2 буквы
            response = character_client.add_character(random_character)

        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)
        characters_to_cleanup.append(random_character["name"])

    @allure.story('Positive: Добавление персонажа и проверка обновления')
    @pytest.mark.parametrize("character", CHARACTER_DATA)
    def test_add_and_update_character(self, character_client, characters_to_cleanup, character):
        response = character_client.add_character(character)
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)
        characters_to_cleanup.append(character["name"])

        updated_character = character.copy()
        updated_character["universe"] = create_random_character()["universe"]
        updated_character["education"] = create_random_character()["education"]
        updated_character["identity"] = create_random_character()["education"]
        updated_character["weight"] = create_random_character()["weight"]
        updated_character["height"] = create_random_character()["height"]
        response = character_client.update_character(updated_character)
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)

    @allure.story('Positive: Проверка создания персонажа с максимальным и минимальным весом и ростом')
    @pytest.mark.parametrize(
        "weight, height",
        [
            (max(CHARACTER_DATA, key=lambda x: x['weight'])['weight'],
             max(CHARACTER_DATA, key=lambda x: x['height'])['height']),
            (min(CHARACTER_DATA, key=lambda x: x['weight'])['weight'],
             min(CHARACTER_DATA, key=lambda x: x['height'])['height'])
        ]
    )
    def test_max_weight_and_height(self, character_client, characters_to_cleanup, weight, height):
        character = create_random_character()
        character["name"] = f"{weight}_{height}_{random.randint(0, 1)} "
        character["weight"] = weight
        character["height"] = height
        response = character_client.add_character(character)
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)
        characters_to_cleanup.append(character["name"])

    ### Negative Tests ###

    @allure.story('Negative: Добавление персонажа, который уже существует')
    @pytest.mark.parametrize("existing_character", CHARACTER_DATA)
    def test_add_existing_character(self, character_client, characters_to_cleanup, existing_character):
        character_client.add_character(existing_character)
        characters_to_cleanup.append(existing_character["name"])
        response = character_client.add_character(existing_character)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @allure.story('Negative: Удаление несуществующего персонажа')
    @pytest.mark.parametrize("name", ["NonExistentName", "AnotherName"])
    def test_delete_non_existent_character(self, character_client, name):
        response = character_client.delete_character(name)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @allure.story('Negative: Добавление персонажа с некорректными данными')
    @pytest.mark.parametrize(
        "invalid_character",
        [
            {"name": "", "universe": "Marvel Universe", "weight": "not_a_number"},
            {"name": "Duplicate", "universe": "", "height": -1},
        ],
    )
    def test_add_invalid_character(self, character_client, invalid_character):
        response = character_client.add_character(invalid_character)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @allure.story('Negative: Получение несуществующего персонажа по имени')
    @pytest.mark.parametrize("character_name", [char["name"] for char in CHARACTER_DATA])
    def test_get_not_exist_character_by_name(self, character_client, character_name):
        response = character_client.get_character_by_name(character_name)
        assert response.status_code == HTTPStatus.BAD_REQUEST


@allure.story('Stress: Параллельное добавление персонажей')
def test_parallel_add_characters(character_client, characters_to_cleanup):
    def create_unique_character():
        character = create_random_character()
        character["name"] = f"_{character["name"]}_"
        return character

    characters = [create_unique_character() for _ in range(10)]

    def add_character_and_cleanup(character):
        response = character_client.add_character(character)
        if response.status_code == HTTPStatus.OK:
            characters_to_cleanup.append(character["name"])
        return response.status_code

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(add_character_and_cleanup, characters))

    assert all(status == HTTPStatus.OK for status in results), "Не все персонажи были добавлены успешно."
