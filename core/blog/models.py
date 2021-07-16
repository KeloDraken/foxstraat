from django.db import models

from core.accounts.models import User

class Blog(models.Model):
    object_id = models.CharField(max_length=11, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    body = models.TextField(null=False, blank=False)
        
    displayed_upvotes = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class News(models.Model):
    text = models.TextField(null=False, blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)