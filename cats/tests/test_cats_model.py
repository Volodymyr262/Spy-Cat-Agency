"""
Tests for SpyCat model validation and methods.
"""

from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from cats.tests.factories import SpyCatFactory


def test_spy_cat_str_representation():
    """
    Test the string representation of the model.
    """
    cat = SpyCatFactory(name="Tom")
    assert str(cat) == "Tom"


def test_spy_cat_negative_experience_validation():
    """
    Test that years_of_experience cannot be negative.
    """
    cat = SpyCatFactory.build(years_of_experience=-1)

    with pytest.raises(ValidationError):
        cat.full_clean()


def test_spy_cat_negative_salary_validation():
    """
    Test that salary cannot be negative.
    """
    cat = SpyCatFactory.build(salary=Decimal("-100.00"))

    with pytest.raises(ValidationError):
        cat.full_clean()
