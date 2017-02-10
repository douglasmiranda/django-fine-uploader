from __future__ import unicode_literals

from django.db import models


class FineFile(models.Model):
    fine_file = models.FileField()

    def __str__(self):
        return self.fine_file.name
