import logging
from http import HTTPStatus

import pytest

from src.api_client import CharacterClient

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="class")
def character_client():
    return CharacterClient()


@pytest.fixture(scope='function')
def characters_to_cleanup(character_client):
    """
    Fixture for cleaning up characters after tests.
    Automatically deletes characters created during the test.
    """
    created_characters = []

    yield created_characters

    # Cleanup only characters created in this test
    for name in created_characters:
        try:
            logger.info(f"Attempting to delete character '{name}'...")
            response = character_client.delete_character(name)
            logger.info(f"Character deletion request URL: {response.request.url}")
            if response.status_code == HTTPStatus.OK:
                logger.info(f"Character '{name}' successfully deleted.")
            elif response.status_code == HTTPStatus.BAD_REQUEST:
                logger.warning(
                    f"Character '{name}' not found or cannot be deleted. Status: {response.status_code}")
            else:
                logger.error(f"Unexpected status code when deleting '{name}': {response.status_code}")
        except Exception as e:
            logger.error(f"Error attempting to delete character '{name}': {str(e)}")


@pytest.fixture(scope='function')
def unique_character_name():
    """
    Generate unique character name for test isolation.
    Uses timestamp to ensure uniqueness.
    """
    import time
    return f"test_character_{int(time.time() * 1000)}"
