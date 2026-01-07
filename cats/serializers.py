"""
Serializers for Cats application.
"""

from rest_framework import serializers

from cats.models import SpyCat
from cats.services import check_breed_exists


class SpyCatSerializer(serializers.ModelSerializer):
    """
    Serializer for SpyCat model.
    Handles validation of the breed using external service.
    """

    class Meta:
        model = SpyCat
        fields = "__all__"

    def validate_breed(self, breed_name):
        """
        Check if the breed exists using TheCatAPI service.
        """
        if not check_breed_exists(breed_name):
            raise serializers.ValidationError(f"Breed '{breed_name}' does not exist.")
        return breed_name


class SpyCatUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer strictly for updating SpyCat.
    Only salary is editable.
    """
    class Meta:
        model = SpyCat
        fields = '__all__'
        read_only_fields = ('name', 'years_of_experience', 'breed')