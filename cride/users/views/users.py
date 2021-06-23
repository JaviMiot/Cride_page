
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# * Serializer methods
from cride.users.serializers import (
    UserLoginSerializer,
    UserSignupSerializer,
    UserModelSerializer,
    AccountVerifySerializer
)


class UserLoginAPIView(APIView):
    """Login API view
    """

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request

        Args:
            request ([type]): [description]
        """

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }

        return Response(data, status=status.HTTP_201_CREATED)


class UserSignupAPIView(APIView):
    """Signup API view
    """

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request

        Args:
            request ([type]): [description]
        """

        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)


class AccountVerifyAPIView(APIView):
    """Account verification API view
    """

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request

        Args:
            request ([type]): [description]
        """

        serializer = AccountVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'message': 'Congratulations, now go share some rides!'
        }

        return Response(data, status=status.HTTP_201_CREATED)
