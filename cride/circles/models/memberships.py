"""model Membership
    """
from django.db import models
from cride.utils.models import CRideModel


class Membership(models.Model):
    """Membership MODEL
     TABLA QUE TIENE RELACIONES
    Args:
        models ([type]): [description]
    """

    user = models.ForeignKey('users.Users', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profiles', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        'circle admin',
        default=False,
        help_text="Circle admins can update tha circle's data and manage its members."
    )

    # * invitations

    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_inv = models.PositiveSmallIntegerField(default=0)

    invited_by = models.ForeignKey(
        'users.Users',
        null=True,
        on_delete=models.SET_NULL,
        related_name='invited_by'
    )

    # * stat

    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)

    # * status
    is_active = models.BooleanField(
        'active status',
        default=False,
        help_text='Only active users are allowed to interact in the circle'
    )

    def __str__(self):
        return f'@{self.user.username} at #{self.circle.slug_name}'