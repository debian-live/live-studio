import datetime

from django.db import models

from .managers import BuildManager

class Build(models.Model):
    config = models.ForeignKey('config.Config')

    enqueued = models.DateTimeField(default=datetime.datetime.utcnow)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    success = models.BooleanField(default=False)

    objects = BuildManager()

    class Meta:
        ordering = ('-enqueued',)
