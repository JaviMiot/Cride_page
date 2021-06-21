# user models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# utilities
from cride.utils.models import CRideModel


class Users(CRideModel, AbstractUser):
    """eXTIENDE DE CALSE ABSTRACTA DE USER 
    cambia el username popr el email como clave primaria 

    Args:
        CRideModel ([type]): [description]
        AbstractModels ([type]): [description]
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email address already exists'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9, 15}$',
        message='phone number must be entered i the format: +999999999. up to 15 digits allowed'
    )

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_cliente = models.BooleanField(
        'client status',
        default=True,
        help_text=(
            'help easily distingush users and perform queries.'
            'clients are the main type of user.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='set to true when the user have verified its email address.'
    )

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username
