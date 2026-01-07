"""
Factories for the Cats.
"""

import factory

from cats.models import SpyCat


class SpyCatFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating SpyCat instances.
    """

    class Meta:
        model = SpyCat

    name = factory.Faker("first_name")
    years_of_experience = factory.Faker("random_int", min=1, max=15)
    breed = "Siamese"
    salary = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
