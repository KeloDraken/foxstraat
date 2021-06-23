from django.db import models

from core.accounts.models import User


class Bulletin(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    caption = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
class BulletinImage(models.Model):
    property = models.ForeignKey(
        Bulletin, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='bulletin/images/')
