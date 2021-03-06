import uuid
import datetime

from django.db import models
from django.conf import settings

from .managers import BuildManager

class Build(models.Model):
    ident = models.CharField(max_length=40, unique=True, default=uuid.uuid4)

    config = models.ForeignKey('config.Config', related_name='builds')

    enqueued = models.DateTimeField(default=datetime.datetime.now)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)

    filename = models.CharField(max_length=100)

    objects = BuildManager()

    class Meta:
        ordering = ('-enqueued',)

    def __unicode__(self):
        return 'Build #%d started by %s (status: %s)' % \
            (self.pk, self.config.user.username, self.status())

    def status(self):
        if self.filename:
            return 'success'
        if self.finished:
            return 'failure'
        if self.started:
            return 'building'
        return 'waiting'

    def log_url(self):
        return '%s/%s/log.txt' % (settings.BUILDS_URL, self.ident)

    def result_url(self):
        return '%s/%s/%s' % (settings.BUILDS_URL, self.ident, self.filename)
