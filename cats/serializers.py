"""
Serializers for Cats application.
"""

from rest_framework import serializers

from cats.models import Mission, SpyCat, Target
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


class TargetSerializer(serializers.ModelSerializer):
    """
    Serializer for Target model.
    """

    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_completed']
        read_only_fields = ['name', 'country']

    def validate(self, data):
        """
        Check if notes are being updated and if it's allowed (Freezing logic).
        """
        if 'notes' in data:
            instance = self.instance
            if instance:
                if instance.is_completed:
                    raise serializers.ValidationError(
                        "Cannot update notes because the target is completed."
                    )
                if instance.mission.is_completed:
                    raise serializers.ValidationError(
                        "Cannot update notes because the mission is completed."
                    )
        return data


class MissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Mission model with nested targets.
    """
    targets = TargetSerializer(many=True)
    cat = serializers.PrimaryKeyRelatedField(
        queryset=SpyCat.objects.all(),
        required=False, allow_null=True
    )

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'is_completed', 'targets']
        read_only_fields = ['is_completed']  # Mission completes automatically

    def validate_targets(self, value):
        """
        Validate that targets count is between 1 and 3.
        """
        if not (1 <= len(value) <= 3):
            raise serializers.ValidationError(
                "A mission must have between 1 and 3 targets."
            )
        return value

    def validate_cat(self, value):
        """
        Check if the assigned cat is already busy with another mission.
        """
        if value:
            qs = Mission.objects.filter(cat=value)

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    "This cat is already assigned to another mission."
                )
        return value

    def create(self, validated_data):
        """
        Custom create method to handle nested targets.
        """
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)

        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)

        return mission
