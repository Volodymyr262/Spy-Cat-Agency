"""
Views for SpyCat application.
"""

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response

from cats.models import Mission, SpyCat, Target
from cats.serializers import (
    AssignCatSerializer,
    MissionSerializer,
    SpyCatSerializer,
    SpyCatUpdateSerializer,
    TargetSerializer,
)


class SpyCatViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing SpyCat instances.
    """

    queryset = SpyCat.objects.all().order_by("-id")

    def get_serializer_class(self):
        """
        Return separate serializers for Create/List and Update actions.
        """
        if self.action in ["update", "partial_update"]:
            return SpyCatUpdateSerializer
        return SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Missions.
    """

    queryset = Mission.objects.all().order_by("-id")
    serializer_class = MissionSerializer

    http_method_names = ["get", "post", "delete", "head", "options"]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except DjangoValidationError as e:
            raise DRFValidationError({"detail": e.messages}) from e

    @action(
        detail=True,
        methods=["post"],
        url_path="assign-cat",
        serializer_class=AssignCatSerializer,
    )
    def assign_cat(self, request, pk=None):
        """
        Custom endpoint to assign a cat to a mission.
        URL: POST /missions/{id}/assign-cat/
        """
        mission = self.get_object()

        serializer = AssignCatSerializer(data=request.data)

        if serializer.is_valid():
            cat_id = serializer.validated_data["cat_id"]
            cat = SpyCat.objects.get(pk=cat_id)

            mission.cat = cat
            mission.save()

            return Response(MissionSerializer(mission).data)

        return Response(serializer.errors, status=400)


class TargetViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet for updating Targets (notes, completion status).
    Creation/Deletion is disabled directly (handled via Mission).
    """

    queryset = Target.objects.all()
    serializer_class = TargetSerializer
