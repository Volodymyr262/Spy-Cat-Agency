"""
Test for models...
Global fixtures for pytest configuration.
"""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """
    Fixture to provide an instance of DRF APIClient.
    Useful for testing API endpoints.
    """
    return APIClient()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enables database access for all tests.
    This removes the need to use @pytest.mark.django_db decorator on every test.
    """
    pass
