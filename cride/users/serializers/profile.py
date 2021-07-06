"""Serializer profile"""


from rest_framework import serializers

from cride.users.models import Profiles


class ProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profiles
        fields = (
            'picture',
            'biography',
            'rides_taken',
            'rides_offered',
            'reputation'
        )

        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'reputation',
        )
