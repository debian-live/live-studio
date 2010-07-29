import uuid
import datetime

from django.db import models

from .managers import BuildManager

class Build(models.Model):
    ident = models.CharField(max_length=40, unique=True, default=uuid.uuid4)

    config = models.ForeignKey('config.Config', related_name='builds')

    enqueued = models.DateTimeField(default=datetime.datetime.utcnow)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    success = models.BooleanField(default=False)

    objects = BuildManager()

    class Meta:
        ordering = ('-enqueued',)
