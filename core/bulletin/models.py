from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from core.accounts.models import User


class Bulletin(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=140, null=False, blank=False)
    yt_embed = models.CharField(max_length=20, null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
class BulletinImage(models.Model):
    bulletin = models.ForeignKey(
        Bulletin, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    upvotes = models.PositiveIntegerField(default=0)
    displayed_upvotes = models.PositiveIntegerField(default=0)
    image = ProcessedImageField(
        upload_to='bulletin/images/',
        processors=[ResizeToFit(480, 600)],
        format='JPEG',
        options={'quality': 90}
    )


class Tag(models.Model):
    object_id = models.CharField(max_length=11, null=True, blank=True)
    name = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return self.name


class PostTag(models.Model):
    post = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    tag = models.ForeignKey(
            Tag,
            on_delete=models.CASCADE,
            related_name='hashtag', 
            max_length=300, 
            null=True, 
            blank=True
        )

    def __str__(self):
        return self.hashtag