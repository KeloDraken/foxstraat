from django.db import models


class Ref(models.Model):
    object_id = models.CharField(max_length=11, null=True, blank=True)
    source = models.CharField(max_length=200, null=False, blank=False)
    hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.source

class News(models.Model):
    text = models.TextField(null=False, blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    body = models.TextField(max_length=2000, null=False, blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

class Rules(models.Model):
    body = models.TextField(null=False, blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)

class Terms(models.Model):
    body = models.TextField(null=False, blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)

class Privacy(models.Model):
    body = models.TextField(null=False, blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)