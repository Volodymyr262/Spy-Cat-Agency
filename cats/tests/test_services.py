"""
Tests for external services integration.
"""

from unittest.mock import Mock, patch

from cats.services import check_breed_exists


@patch("cats.services.requests.get")
def test_check_breed_exists_found(mock_get):
    """
    Test that check_breed_exists returns True if breed is in the list.
    We mock the API response with data provided by the user.
    """
    # Mocking the response from TheCatAPI
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "id": "abys",
            "name": "Abyssinian",
            "temperament": "Active",
        },
        {
            "id": "beng",
            "name": "Bengal",
            "temperament": "Alert",
        },
    ]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Act
    result = check_breed_exists("Bengal")

    # Assert
    assert result is True
    mock_get.assert_called_once()


@patch("cats.services.requests.get")
def test_check_breed_exists_not_found(mock_get):
    """
    Test that check_breed_exists returns False if breed is NOT in the list.
    """
    mock_response = Mock()
    mock_response.json.return_value = [{"id": "abys", "name": "Abyssinian"}]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Act: "Dog" is clearly not in the mocked list
    result = check_breed_exists("Dog")

    # Assert
    assert result is False
