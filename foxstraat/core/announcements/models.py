from django.db import models


class Announcement(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    title = models.CharField(max_length=70, null=False, blank=False)
    body = models.TextField(max_length=140)
    is_default = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
