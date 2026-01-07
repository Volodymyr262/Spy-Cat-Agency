"""
Integration tests for Mission API.
"""
from django.urls import reverse
from rest_framework import status

from cats.models import Mission, Target
from cats.tests.factories import MissionFactory, SpyCatFactory


def test_create_mission_with_targets_success(api_client):
    """
    Test creating a mission with 2 targets (Happy Path).
    """
    cat = SpyCatFactory()
    url = reverse('mission-list')

    payload = {
        "cat": cat.id,
        "targets": [
            {"name": "Target 1", "country": "US", "notes": "Plan A"},
            {"name": "Target 2", "country": "GB", "notes": "Plan B"}
        ]
    }

    response = api_client.post(url, payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Mission.objects.count() == 1
    assert Target.objects.count() == 2

    mission = Mission.objects.first()
    assert mission.cat == cat
    assert mission.targets.count() == 2


def test_create_mission_validation_limits(api_client):
    """
    Test validation: min 1 target, max 3 targets.
    """
    cat = SpyCatFactory()
    url = reverse('mission-list')

    payload_empty = {"cat": cat.id, "targets": []}
    resp_empty = api_client.post(url, payload_empty, format='json')
    assert resp_empty.status_code == status.HTTP_400_BAD_REQUEST
    assert "targets" in resp_empty.data

    payload_many = {
        "cat": cat.id,
        "targets": [{"name": "T", "country": "US"} for _ in range(4)]
    }
    resp_many = api_client.post(url, payload_many, format='json')
    assert resp_many.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_mission_assigned_to_cat(api_client):
    """
    Test that we cannot delete a mission if it is assigned to a cat.
    """
    mission = MissionFactory()
    url = reverse('mission-detail', args=[mission.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Mission.objects.count() == 1


def test_delete_mission_unassigned(api_client):
    """
    Test that we CAN delete a mission if no cat is assigned.
    """
    mission = MissionFactory(cat=None)
    url = reverse('mission-detail', args=[mission.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Mission.objects.count() == 0


def test_assign_cat_to_existing_mission(api_client):
    """
    Test assigning a free cat to a mission that was created without a cat.
    """
    mission = MissionFactory(cat=None)
    free_cat = SpyCatFactory()

    url = reverse('mission-detail', args=[mission.id])
    payload = {"cat": free_cat.id}

    response = api_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_200_OK

    mission.refresh_from_db()
    assert mission.cat == free_cat


def test_cannot_assign_busy_cat_to_mission(api_client):
    """
    Test that we cannot assign a cat to a mission if
    the cat is already assigned to another mission.
    Should return 400 Bad Request (Business Logic Error), not 500 IntegrityError.
    """
    busy_cat = SpyCatFactory()
    MissionFactory(cat=busy_cat)

    mission_b = MissionFactory(cat=None)

    url = reverse('mission-detail', args=[mission_b.id])
    payload = {"cat": busy_cat.id}

    response = api_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cat" in response.data
