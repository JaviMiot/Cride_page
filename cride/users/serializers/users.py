"""users serializer"""

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

#* models
from cride.users.models import Users

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields =(
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserLoginSerializer(serializers.Serializer):
    """user login serializer
    handle the login request data

    Args:
        serializers ([type]): [description]
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        "check credetials"
        user = authenticate(username=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token

        Args:
            data ([type]): [description]
        """

        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
