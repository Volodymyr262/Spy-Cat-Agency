"""
Views for Cats application.
"""

from rest_framework import viewsets

from cats.models import SpyCat
from cats.serializers import SpyCatSerializer, SpyCatUpdateSerializer


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