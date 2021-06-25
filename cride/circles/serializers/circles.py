
# * Circles serializers

# * Djengo rest
from rest_framework import serializers

# * Model
from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):
    """circle model serializer

    Args:
        serializers ([type]): [description]
    """
    members_limit = serializers.IntegerField(
        required=True,
        min_value=10,
        max_value=32000,
    )

    is_limited = serializers.BooleanField(default=False)

    class Meta:

        model = Circle

        fields = (
            'id', 'name', 'slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'is_limited', 'members_limit'
        )

        read_only_fields = (
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken',
        )

    def validate(self, data):
        """Ensure both membes_limits an is limit are presentes

        Args:
            data ([type]): [description]
        """

        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)

        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circles is limited, a member limit musr be provided')

        return data
