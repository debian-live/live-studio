import uuid
import datetime

from django.db import models
from django.conf import settings

from .managers import BuildManager

class Build(models.Model):
    ident = models.CharField(max_length=40, unique=True, default=uuid.uuid4)

    config = models.ForeignKey('config.Config', related_name='builds')

    enqueued = models.DateTimeField(default=datetime.datetime.utcnow)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)

    filename = models.CharField(max_length=50)

    objects = BuildManager()

    class Meta:
        ordering = ('-enqueued',)

    def status(self):
        if self.filename:
            return 'success'
        if self.finished:
            return 'failure'
        if self.started:
            return 'building'
        return 'waiting'

    def result_url(self):
        return '%s/%s/%s' % (settings.BUILDS_URL, self.ident, self.filename)
