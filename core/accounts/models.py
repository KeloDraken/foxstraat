from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    object_id = models.CharField(max_length=20, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)
    custom_styles = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username