"""
Signals for Cats application.
Handles automated business logic.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from cats.models import Target


@receiver(post_save, sender=Target)
def check_mission_completion(sender, instance, **kwargs):
    """
    Signal receiver that checks if all targets for a mission are completed.
    If so, marks the mission as completed.
    """
    mission = instance.mission

    if mission.is_completed:
        return

    has_incomplete_targets = mission.targets.filter(is_completed=False).exists()

    if not has_incomplete_targets:
        mission.is_completed = True
        mission.save()
