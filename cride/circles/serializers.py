"""* Circle serializers"""

# * Django rest Framework
from cride.circles.models.circles import Circle
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class CircleSerializer(serializers.Serializer):
    """Cricle serializer

    Args:
        serializers ([type]): [description]
    """

    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
    """Crea un serializer al crear circulo

    Args:
        serializers ([type]): [description]
    """
    name = serializers.CharField(max_length=140)

    #Hago la validación que sea unico
    slug_name = serializers.SlugField(
        max_length=40,
        validators=[
            UniqueValidator(queryset=Circle.objects.all()),
        ]
    )
    about = serializers.CharField(max_length=255, required=False)

    def create(self, data):
        """Craete Circle Serializer

        Args:
            data ([type]): [description]
        """
        return Circle.objects.create(**data)
