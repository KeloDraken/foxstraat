from django.db import models


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


class ForbiddenWebsites(models.Model):
    protocol = models.CharField(max_length=20000, null=True, blank=True)
    domain = models.CharField(max_length=200000, null=True, blank=True)
    path = models.CharField(max_length=20000, null=True, blank=True)
    subdomain = models.CharField(max_length=20000, null=True, blank=True)
    host = models.CharField(max_length=20000, null=True, blank=True)
    tld = models.CharField(max_length=20000, null=True, blank=True)
    parent_domain = models.CharField(max_length=20000, null=True, blank=True)

    def __str__(self) -> str:
        return self.domain
