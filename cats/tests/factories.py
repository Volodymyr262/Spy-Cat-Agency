"""
Factories for the Cats.
"""

import factory

from cats.models import Mission, SpyCat, Target


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


class MissionFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Mission instances.
    """

    class Meta:
        model = Mission
        skip_postgeneration_save = True

    cat = factory.SubFactory(SpyCatFactory)
    is_completed = False

    @factory.post_generation
    def related_targets(self, create, count, **kwargs):
        """
        Custom hook to create targets for the mission.
        Usage: MissionFactory(related_targets=3) creates a mission with 3 targets.
        """
        if not create:
            return

        if count:
            TargetFactory.create_batch(count, mission=self)


class TargetFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Target instances.
    """

    class Meta:
        model = Target

    mission = factory.SubFactory(MissionFactory)

    name = factory.Faker("name")
    country = factory.Faker("country")
    notes = factory.Faker("text")
    is_completed = False
