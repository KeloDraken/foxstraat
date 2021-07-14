from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from core.accounts.models import User


class Bulletin(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=140, null=False, blank=False)
    
    image = ProcessedImageField(
        upload_to='bulletin/images/',
        processors=[ResizeToFit(480, 600)],
        format='JPEG',
        options={'quality': 90},
        null=True
    )
    displayed_upvotes = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    caption = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


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


class Song(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    cover_art = ProcessedImageField(
        upload_to='bulletin/music/cover_art/',
        processors=[ResizeToFit(480, 600)],
        format='JPEG',
        options={'quality': 90},
        null=True
    )

    spotify = models.URLField(max_length=200, null=True, blank=True)
    soundcloud = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)
    
    displayed_upvotes = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)