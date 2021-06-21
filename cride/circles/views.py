# * Rest framework django
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from cride.circles.models import Circle
# * Serializer
from cride.circles.serializers import (CircleSerializer,
                                       CreateCircleSerializer
                                       )
# * se decora la clase y solo será llamada por api rest Django


@api_view(['GET'])
def list_circles(request):
    circles = Circle.objects.all()
    public = circles.filter(is_public=True)
    # *  Para convertir multiples queries a json
    serializer = CircleSerializer(public, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def create_circle(request):
    """Create circle

    Args:
        request ([type]): [description]
    """
    # * HACE VALIDACION
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # * creo el circulo
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)
