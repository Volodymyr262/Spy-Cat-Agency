"""
Integration tests for Cats API endpoints.
"""

from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from cats.models import SpyCat
from cats.tests.factories import SpyCatFactory

CATS_URL = reverse("spycat-list")


def test_list_cats(api_client):
    """
    Test retrieving a list of spy cats.
    """
    SpyCatFactory.create_batch(3)

    response = api_client.get(CATS_URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@patch("cats.serializers.check_breed_exists")
def test_create_cat_success(mock_check_breed, api_client):
    """
    Test creating a spy cat with valid data and validated breed.
    """
    # Arrange
    mock_check_breed.return_value = True
    payload = {
        "name": "Bond",
        "years_of_experience": 7,
        "breed": "Siberian",
        "salary": "75000.00",
    }

    response = api_client.post(CATS_URL, payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == payload["name"]
    assert response.data["breed"] == "Siberian"


@patch("cats.serializers.check_breed_exists")
def test_create_cat_invalid_breed(mock_check_breed, api_client):
    """
    Test that creating a cat with a non-existent breed fails.
    """
    mock_check_breed.return_value = False
    payload = {
        "name": "FailCat",
        "years_of_experience": 2,
        "breed": "Unicorn",  # Invalid breed
        "salary": "20000.00",
    }

    response = api_client.post(CATS_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "breed" in response.data


def test_retrieve_single_cat(api_client):
    """
    Test retrieving a single spy cat by ID.
    """
    cat = SpyCatFactory(name="Solo")
    url = reverse("spycat-detail", args=[cat.id])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Solo"


def test_delete_cat(api_client):
    """
    Test removing a spy cat from the system.
    """
    cat = SpyCatFactory()
    url = reverse("spycat-detail", args=[cat.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert SpyCat.objects.count() == 0


def test_update_cat_salary(api_client):
    """
    Test updating spy cat's salary.
    """
    cat = SpyCatFactory(salary="500.00")
    url = reverse("spycat-detail", args=[cat.id])

    payload = {"salary": "1000.00"}

    response = api_client.patch(url, payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["salary"] == "1000.00"

    cat.refresh_from_db()
    assert cat.salary == 1000.00


def test_update_cat_other_fields_restricted(api_client):
    """
    Test that updating other fields (name, breed) is NOT allowed or ignored.
    According to requirements: 'Ability to update spy cats’ information (Salary)'.
    """
    cat = SpyCatFactory(name="Bond", breed="Siberian")
    url = reverse("spycat-detail", args=[cat.id])

    payload = {"name": "Villain", "breed": "Persian", "salary": "1000.00"}

    response = api_client.patch(url, payload)

    assert response.status_code == status.HTTP_200_OK

    cat.refresh_from_db()
    assert cat.salary == 1000.00  # changed
    assert cat.name == "Bond"  # the same
    assert cat.breed == "Siberian"  # the same
