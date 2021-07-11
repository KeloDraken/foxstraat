from django.db import models


class Ref(models.Model):
    source = models.CharField(max_length=200, null=False, blank=False)
    hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.source