import argparse
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration from environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "http://rest.test.ivi.ru/v2")
API_USERNAME = os.getenv("API_USERNAME", "")
API_PASSWORD = os.getenv("API_PASSWORD", "")

if not API_USERNAME or not API_PASSWORD:
    raise ValueError("API_USERNAME and API_PASSWORD must be set in environment variables or .env file")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_all_characters():
    """ Get all characters from API and return a list. """
    session = requests.Session()
    session.auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)
    try:
        logger.info(f"Sending request: GET {API_BASE_URL}/characters")
        response = session.get(f"{API_BASE_URL}/characters")
        response.raise_for_status()
        data = response.json()
        logger.info("Data successfully retrieved.")
        return data.get("result", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Request execution error: {e}")
        return []
    except ValueError as e:
        logger.error(f"JSON parsing error: {e}")
        return []

def filter_characters_by_criteria(characters, **criteria):
    """ Return a list of character names matching the criteria. """
    matched_characters = []
    for character in characters:
        if all((criteria[key] is None or character.get(key) == criteria[key]) for key in criteria):
            matched_characters.append(character)  # save entire object to display all data
            logger.info(f"Found character: {character.get('name')}")
            # output character JSON parameters
            logger.info(f"Character information: {json.dumps(character, ensure_ascii=False, indent=4)}")
    return matched_characters

def delete_characters_by_name(character_names, limit=None):
    """ Delete characters by names up to the specified limit. """
    session = requests.Session()
    session.auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)
    deletion_count = 0

    for character in character_names:
        name = character.get('name')
        if limit is not None and deletion_count >= limit:
            break
        try:
            logger.info(f"Deleting character: {name}")
            response = session.delete(f"{API_BASE_URL}/character", params={'name': name})
            response.raise_for_status()
            deletion_count += 1
            logger.info(f"Character {name} successfully deleted.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting {name}: {e}")

    logger.info(f"Total {deletion_count} characters deleted.")

def main(perform_search=False, perform_deletion=False, limit=None, **criteria):
    """ Main script logic: search and delete characters by criteria. """
    all_characters = get_all_characters()
    matched_characters = filter_characters_by_criteria(all_characters, **criteria)

    if perform_search:
        total_count = len(matched_characters)
        if total_count > 0:
            logger.info(f"Found {total_count} matching characters.")
        else:
            logger.info("No matching characters found.")

    if perform_deletion:
        delete_characters_by_name(matched_characters, limit=limit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search and delete characters by criteria.')
    parser.add_argument('--search', action='store_true', help='Search characters.')
    parser.add_argument('--delete', action='store_true', help='Delete characters.')
    parser.add_argument('--limit', type=int, default=None, help='Limit on the number of characters to delete.')
    parser.add_argument('--education', type=str, help='Education criterion.')
    parser.add_argument('--height', type=int, help='Height criterion.')
    parser.add_argument('--identity', type=str, help='Identity criterion.')
    parser.add_argument('--other_aliases', type=str, help='Other aliases criterion.')
    parser.add_argument('--universe', type=str, help='Universe criterion.')
    parser.add_argument('--weight', type=float, help='Weight criterion.')
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
