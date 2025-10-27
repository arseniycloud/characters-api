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

    @allure.story('Positive: Get all characters')
    def test_get_characters(self, character_client):
        response = character_client.get_characters()
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharactersListSchema)

        # Validate response body structure
        assert "result" in data
        assert isinstance(data["result"], list)

    @allure.story('Positive: Get character by name')
    @pytest.mark.parametrize("character", MOST_COMMON_CHARACTER_NAMES)
    def test_get_character_by_name(self, character_client, character):
        response = character_client.get_character_by_name(character)
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)

        # Validate response body structure and content
        assert "result" in data
        assert isinstance(data["result"], dict)
        assert "name" in data["result"]
        assert data["result"]["name"] == character

    @allure.story('Positive: Add character with fake data')
    def test_add_character_with_faker(self, character_client, characters_to_cleanup):
        random_character = create_random_character()
        response = character_client.add_character(random_character)

        # Check if character already exists
        while response.status_code == HTTPStatus.BAD_REQUEST:
            random_character["name"] = random_character["name"][:-2]  # Shorten name by 2 characters
            response = character_client.add_character(random_character)

        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)

        # Validate response body structure and content
        assert "result" in data
        assert isinstance(data["result"], dict)
        assert "name" in data["result"]
        assert data["result"]["name"] == random_character["name"]

        characters_to_cleanup.append(random_character["name"])

    @allure.story('Positive: Add character and verify update')
    @pytest.mark.parametrize("character", CHARACTER_DATA)
    def test_add_and_update_character(self, character_client, characters_to_cleanup, character):
        response = character_client.add_character(character)
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)

        # Validate initial character data in response
        assert "result" in data
        assert data["result"]["name"] == character["name"]
        assert data["result"]["universe"] == character.get("universe")

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

        # Validate updated character data in response
        assert "result" in data
        assert data["result"]["name"] == character["name"]
        assert data["result"]["universe"] == updated_character["universe"]
        assert data["result"]["education"] == updated_character["education"]

    @allure.story('Positive: Verify character creation with max and min weight and height')
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
        character["weight"] = weight
        character["height"] = height
        response = character_client.add_character(character)
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        character_client.validate_response(data, CharacterResponseSchema)

        # Validate weight and height in response
        assert "result" in data
        assert data["result"]["weight"] == weight
        assert data["result"]["height"] == height

        characters_to_cleanup.append(character["name"])

    ### Negative Tests ###

    @allure.story('Negative: Add existing character')
    @pytest.mark.parametrize("existing_character", CHARACTER_DATA)
    def test_add_existing_character(self, character_client, characters_to_cleanup, existing_character):
        character_client.add_character(existing_character)
        characters_to_cleanup.append(existing_character["name"])
        response = character_client.add_character(existing_character)
        assert response.status_code == HTTPStatus.BAD_REQUEST

        # Validate error response body
        data = response.json()
        assert "detail" in data or "message" in data

    @allure.story('Negative: Delete non-existent character')
    @pytest.mark.parametrize("name", ["NonExistentName", "AnotherName"])
    def test_delete_non_existent_character(self, character_client, name):
        response = character_client.delete_character(name)
        assert response.status_code == HTTPStatus.BAD_REQUEST

        # Validate error response body
        data = response.json()
        assert "detail" in data

    @allure.story('Negative: Add character with invalid data')
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

        # Validate error response body
        data = response.json()
        assert "detail" in data

    @allure.story('Negative: Get non-existent character by name')
    @pytest.mark.parametrize("character_name", [char["name"] for char in CHARACTER_DATA])
    def test_get_not_exist_character_by_name(self, character_client, character_name):
        response = character_client.get_character_by_name(character_name)
        assert response.status_code == HTTPStatus.BAD_REQUEST

        # Validate error response body
        data = response.json()
        assert "detail" in data


@allure.story('Stress: Parallel character addition')
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

    assert all(status == HTTPStatus.OK for status in results), "Not all characters were added successfully."
