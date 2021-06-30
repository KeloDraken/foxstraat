from django.db import models


class Category(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return self.name


class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=11, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    url_string = models.CharField(max_length=100, null=False, blank=False)
    about = models.CharField(max_length=240, null=True, blank=True)
    
    