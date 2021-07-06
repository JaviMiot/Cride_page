

from rest_framework import mixins, status, viewsets
from rest_framework import response
from rest_framework.response import Response
from rest_framework.decorators import action

from cride.users.models import Users
from cride.circles.models import Circle
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers.profile import ProfileModelSerializer
# * permisions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from cride.users.permissions import IsAccountOwner

# * Serializer methods
from cride.users.serializers import (
    UserLoginSerializer,
    UserSignupSerializer,
    UserModelSerializer,
    AccountVerifySerializer
)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """user view set
    handle sign up, login and accointy verifications

    Args:
        viewsets ([type]): [description]

    Returns:
        [type]: [description]
    """
    queryset = Users.objects.filter(is_active=True, is_cliente=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Asiigna permision basadas en una accion"""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action == ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]

        return [permision() for permision in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """users sign up"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """"User signup"""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        serializer = AccountVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'message': 'Congratulations, now go share some rides!'
        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put','patch'])
    def profile(self,request,*args, **kwargs):
        """update profile data"""
        user = self.get_object()
        profile = user.profiles
        partial = request.method == 'PATH'
        serializer = ProfileModelSerializer(
            profile,
            data = request.data,
            partial = partial
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self,request, *args, **kwargs):
        """datros extras para el response"""
        response = super(UserViewSet,self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members = request.user,
            membership__is_active = True
        )

        data = {
            'user': response.data,
            'circle':CircleModelSerializer(circles, many=True).data,
    
        }

        response.data = data
        return response