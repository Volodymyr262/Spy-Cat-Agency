"""
Tests for Django Signals (Business Logic Side Effects).
"""

from cats.tests.factories import MissionFactory, TargetFactory


def test_mission_remains_incomplete_if_targets_pending():
    """
    Test that mission stays is_completed=False if there are still unfinished targets.
    """
    mission = MissionFactory(is_completed=False)
    target1 = TargetFactory(mission=mission, is_completed=False)
    _ = TargetFactory(mission=mission, is_completed=False)

    target1.is_completed = True
    target1.save()

    mission.refresh_from_db()
    assert mission.is_completed is False


def test_mission_auto_completes_when_all_targets_done():
    """
    Test that mission becomes is_completed=True automatically
    when the LAST target is marked as completed.
    """
    mission = MissionFactory(is_completed=False)
    _ = TargetFactory(mission=mission, is_completed=True)
    target2 = TargetFactory(mission=mission, is_completed=False)

    target2.is_completed = True
    target2.save()

    mission.refresh_from_db()
    assert mission.is_completed is True
