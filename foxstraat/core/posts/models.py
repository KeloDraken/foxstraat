from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from foxstraat.core.accounts.models import User


class Post(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    url = models.URLField(max_length=1000, null=False, blank=False)
    title = models.CharField(max_length=400, null=False, blank=False)
    image = models.CharField(max_length=100000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    publisher = models.CharField(max_length=400, null=False, blank=False)

    score = models.IntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    bulletin = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    has_voted = models.BooleanField(default=False)
