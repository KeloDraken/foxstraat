from django.db import models

from core.accounts.models import User


class Link(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    link = models.URLField(max_length=1000, null=False, blank=False)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)
    date_created = models.DateField(auto_now_add=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

class LinkVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    biltins = models.ForeignKey(Link, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    has_voted = models.BooleanField(default=False)
    
