"""
Tests for Mission and Target models using Factory Boy.
"""

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from cats.models import Mission
from cats.tests.factories import MissionFactory, SpyCatFactory


def test_one_cat_one_mission_constraint():
    """
    Test that a cat can have only one mission (OneToOne relationship).
    """
    cat = SpyCatFactory()

    MissionFactory(cat=cat)

    with pytest.raises(IntegrityError):
        MissionFactory(cat=cat)


def test_prevent_deletion_if_assigned_to_cat():
    """
    Test requirement: A mission cannot be deleted if it is already assigned to a cat.
    """
    mission = MissionFactory()

    with pytest.raises(
        ValidationError, match="Cannot delete mission assigned to a cat"
    ):
        mission.delete()


def test_allow_deletion_if_not_assigned():
    """
    Test that an unassigned mission CAN be deleted.
    """
    mission = MissionFactory(cat=None)
    mission_id = mission.id

    mission.delete()

    assert Mission.objects.filter(id=mission_id).exists() is False
