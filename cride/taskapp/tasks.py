from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

import jwt

# * celery
from celery.decorators import task, periodic_task

# * model user
from cride.users.models import Users
from cride.rides.models import Ride

import time
from datetime import timedelta


def gen_verification_token(user):
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


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """send confirmation verification link to given user

    Args:
        user ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """

    for i in range(30):
        time.sleep(1)
        print(f'sleeping {i+1}')

    user = Users.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = f'Welcome @{user.username} verify your count to start using Comparte Ride'
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()


@periodic_task(name="disable_finished_rides", run_every=timedelta(seconds=5))
def disable_finished_rides():
    """disable finish rides"""
    now = timezone.now()
    offset = now +  timedelta(seconds=5)

    #? updtate rides that have already finished
    rides = Ride.objects.filter(
        arrival_date__gte = now,
        arrival_date__lte=offset,
        is_active=True
    )

    rides.update(is_active=False)
