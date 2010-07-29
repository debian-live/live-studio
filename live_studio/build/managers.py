from django.db import models

class BuildManager(models.Manager):
    def pop(self):
        return self.filter(started__isnull=True)[0]
