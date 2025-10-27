import random
from faker import Faker
from src.models import Character

fake = Faker()

# Example lists for random selection
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
    name = fake.first_name()
    universe = random.choice(universes)
    education = random.choice(educations)
    weight = random.choice(weights)
    height = random.choice(heights)
    identity = random.choice(identities)

    return Character(
        name=name,
        universe=universe,
        education=education,
        weight=weight,
        height=height,
        identity=identity
    ).to_dict()
