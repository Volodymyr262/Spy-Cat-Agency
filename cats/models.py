"""
Models for the Cats application.
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
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


class Mission(models.Model):
    """
    Represents a Mission assigned to a Spy Cat.
    """

    cat = models.OneToOneField(
        SpyCat, on_delete=models.SET_NULL, null=True, blank=True, related_name="mission"
    )
    is_completed = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        """
        Override delete method to prevent deletion if assigned to a cat.
        """
        if self.cat:
            raise ValidationError("Cannot delete mission assigned to a cat.")
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Mission {self.id} (Cat: {self.cat})"


class Target(models.Model):
    """
    Represents a Target within a Mission.
    """

    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE, related_name="targets"
    )
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
