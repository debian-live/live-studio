import datetime

from django.db import models

class Entry(models.Model):
    config = models.ForeignKey('config.Config')
    created = models.DateTimeField(default=datetime.datetime.utcnow)
