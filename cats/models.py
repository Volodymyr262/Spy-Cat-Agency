"""
Models for the Cats application.
"""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class SpyCat(models.Model):
    """
    Represents a Spy Cat in the agency.
    """

    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)

    salary = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    def __str__(self):
        return self.name
