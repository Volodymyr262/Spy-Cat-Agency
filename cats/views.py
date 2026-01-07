"""
Views for SpyCat application.
"""
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError as DRFValidationError

from cats.models import Mission, SpyCat, Target
from cats.serializers import (
    MissionSerializer,
    SpyCatSerializer,
    SpyCatUpdateSerializer,
    TargetSerializer,
)


class SpyCatViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing SpyCat instances.
    """
    queryset = SpyCat.objects.all().order_by('-id')

    def get_serializer_class(self):
        """
        Return separate serializers for Create/List and Update actions.
        """
        if self.action in ['update', 'partial_update']:
            return SpyCatUpdateSerializer
        return SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Missions.
    Inherits from ModelViewSet to support Create (POST), List (GET), etc.
    """
    queryset = Mission.objects.all().order_by('-id')
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method.
        We need to catch Django's native ValidationError (raised by the Model)
        and convert it to DRF's ValidationError (so the client gets 400 Bad Request).
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except DjangoValidationError as e:
            raise DRFValidationError({'detail': e.messages})


class TargetViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    ViewSet for updating Targets (notes, completion status).
    Creation/Deletion is disabled directly (handled via Mission).
    """
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
