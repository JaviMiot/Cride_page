from django.db import models
from django.db.models.fields import proxy


class CRideModel(models.Model):
    """Clase abstracta del modelo tiene los siguientes campos
    + created(datetime): almacena la fecha de creacion del
    + modified(datetime): almacena fecha cuando se modifica

    Args:
        models ([type]): [description]
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created')

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was created')

    class Meta:
        abstract =  True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']

