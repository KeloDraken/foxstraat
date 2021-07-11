from django.db import models


class Ref(models.Model):
    source = models.CharField(max_length=200, null=False, blank=False)
    