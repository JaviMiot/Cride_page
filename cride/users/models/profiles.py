# * profile models are

from django.db import models
from cride.utils.models import CRideModel


class Profiles(CRideModel):

    """Profile models 
    A profile hold a users public data like biography and picture
    """

    users = models.OneToOneField('users.Users', on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )

    biography = models.TextField(
        max_length=500,
        blank=True
    )

    # * statictics *
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    reputation = models.FloatField(
        default=5.0,
        help_text="User's reputatio based on the rides taken and offered"
    )

    def __str__(self):
        return str(self.users)
