import logging
import random

import allure
from faker import Faker
from locust import HttpUser, TaskSet, task, between

import config
from src.api_client import CharacterClient
from src.models import Character

# Setup logging
logging.basicConfig(
    filename='test_report.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Faker for generating random data
fake = Faker()

# Example data for random selection
educations = [
    "High school graduate", "College graduate", "Ph.D. in Biophysics", "Unrevealed",
    "Military training", "FBI training", "High school dropout", "University graduate",
    "Some university-level courses", "Doctorate in Medicine"
]

identities = [
    "Secret", "Publicly known", "Known to authorities", "No dual identity",
    "Secret (known to certain government officials)", "Known to intergalactic authorities",
    "Not known to the general populace of Earth"
]

universes = [
    "Marvel Universe", "Earth-712", "Wildways ('Mojoverse')", "Marvel Universe; formerly Earth-4935"
]

heights = [163.0, 197.0, 187.0, 172.0, 210.0, 180.0, 162.0, 154.0, 152.0, 193.0, 200.0, 180.0, 185.0, 170.0,
           287.0]
weights = [103.0, 122.0, 78.0, 67.5, 45.45, 191.25, 108.0, 82.35, 150.0, 146.0, 59.0, 104.0, 101.25, 438.75,
           90.0]


def create_random_character():
    """Create a Character object with random data."""
    return Character(
        name=f"load_{fake.first_name()}",
        universe=random.choice(universes),
        education=random.choice(educations),
        weight=111,
        height=111,
        identity=random.choice(identities)
    ).to_dict()


class APITasks(TaskSet):

    def on_start(self):
        self.api_client = CharacterClient()

    @task
    @allure.story("Get characters list")
    def test_get_characters(self):
        """Send a request to get character list and log the result."""
        response = self.api_client.get_characters()
        if response.status_code == 200:
            logger.info(f"Retrieved characters: {response.json()}")
        else:
            logger.error(f"Error retrieving characters: {response.status_code}")

    @task
    @allure.story("Create new random character")
    def test_create_random_character(self):
        """Create a new random character and log the result."""
        character_data = create_random_character()
        response = self.api_client.add_character(character_data)
        if response.status_code == 200:
            self.last_created_character_name = character_data['name']
            logger.info(f"Created new character: {self.last_created_character_name}")
        else:
            logger.error(f"Error creating character: {response.status_code}")

    @task
    @allure.story("Delete randomly created character")
    def test_delete_character(self):
        """Delete the last created character and log the result."""
        if hasattr(self, 'last_created_character_name'):
            response = self.api_client.delete_character(self.last_created_character_name)
            if response.status_code == 200:
                logger.info(f"Deleted character: {self.last_created_character_name}")
            else:
                logger.error(f"Error deleting character: {response.status_code}")


class WebsiteUser(HttpUser):
    tasks = [APITasks]
    wait_time = between(1, 5)
    host = config.API_URLS['prod']
