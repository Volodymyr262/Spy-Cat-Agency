"""
Services for interacting with external APIs.
"""

import requests


def check_breed_exists(breed_name: str) -> bool:
    """
    Validates if the breed exists using TheCatAPI.
    Fetches the list of all breeds and checks if the given name is present.

    Args:
        breed_name (str): The name of the breed to check.

    Returns:
        bool: True if breed exists, False otherwise.
    """
    url = "https://api.thecatapi.com/v1/breeds"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            breeds_data = response.json()
            for breed in breeds_data:
                if breed.get("name").lower() == breed_name.lower():
                    return True
        return False
    except requests.RequestException:
        # In case of API failure, we might want to log it.
        # For this task, strictly speaking, if we can't verify, return False.
        return False
