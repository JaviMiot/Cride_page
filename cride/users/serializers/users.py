"""users serializer"""

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from django.core.validators import RegexValidator
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.utils import timezone
from datetime import timedelta
import jwt
from django.conf import settings
# * models
from cride.users.models import Users, Profiles


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserSignupSerializer(serializers.Serializer):
    """usersignupserializer
    tiene los datos de registro y crea un usuario/perfil

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='phone number must be entered in the format: +999999999. up to 15 digits allowed'
    )

    phone_number = serializers.CharField(
        validators=[phone_regex],
        max_length=17,
    )

    password = serializers.CharField(
        min_length=8,
        max_length=64
    )

    passwordConfirmation = serializers.CharField(
        min_length=8,
        max_length=64
    )

    first_name = serializers.CharField(
        min_length=2,
        max_length=30
    )

    last_name = serializers.CharField(
        min_length=2,
        max_length=30
    )

    def validate(self, data):
        """Valida los campos

        Args:
            data ([type]): [description]

        Raises:
            serializers.ValidationError: [description]

        Returns:
            [type]: [description]
        """

        password = data['password']
        password_conf = data['passwordConfirmation']

        if password != password_conf:
            raise serializers.ValidationError("Passwords don't match")

        password_validation.validate_password(password)

        return data

    def create(self, data):
        """Crea usuario y perfil

        Args:
            data ([type]): [description]

        Raises:
            serializers.ValidationError: [description]

        Returns:
            [type]: [description]
        """

        data.pop('passwordConfirmation')
        # * para verificar que este verificado
        user = Users.objects.create_user(**data, is_verified=False)
        profile = Profiles.objects.create(users=user)
        self.send_confirmation_email(user=user)
        return user

    def send_confirmation_email(self, user):
        """send confirmation verification link to given user

        Args:
            user ([type]): [description]

        Raises:
            serializers.ValidationError: [description]
            serializers.ValidationError: [description]

        Returns:
            [type]: [description]
        """
        verification_token = self.gen_verification_token(user)
        subject = f'Welcome @{user.username} verify your count to start using Comparte Ride'
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """create JWT token taht user can use to verify its count

        Args:
            user ([type]): [description]

        Raises:
            serializers.ValidationError: [description]
            serializers.ValidationError: [description]

        Returns:
            [type]: [description]
        """
        exp_data = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_data.timestamp()),
            'type': 'email_confirmation'
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token


class AccountVerifySerializer(serializers.Serializer):
    """Account verification serializer

    Args:
        serializers ([type]): [description]]

    Returns:
        [type]: [description]
    """

    token = serializers.CharField()

    def validate_token(self, data):
        try:
            payload = jwt.decode(
                data,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        except jwt.exceptions.PyJWTError:
            raise serializers.ValidationError('Invalid Token Py')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid Token')
        
        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status

        Raises:
            serializers.ValidationError: [description]
            serializers.ValidationError: [description]

        Returns:
            [type]: [description]
        """
        payload = self.context['payload']
        user =  Users.objects.get(username=payload['user'])
        user.is_verified =  True
        user.save()
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
        # verifica si esta verificado el usuario
        if not user.is_verified:
            raise serializers.ValidationError('Is not Active yeat')
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
