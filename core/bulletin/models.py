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
    GENRES = [
        # Rock and metal
        ('Rock','Rock'),
        ('Punk rock','Punk rock'),
        ('Indie rock','Indie rock'),
        ('Alternative rock','Alternative rock'),
        ('Pop rock','Pop rock'),
        ('Hard rock','Hard rock'),
        ('Heavy metal','Heavy metal'),
        ('Grunge','Grunge'),
        ('Emo','Emo'),

        # Pop
        ('Pop','Pop'),
        ('Indie','Indie'),
        ('Hip hop','Hip hop'),
        ('Country','Country'),
        ('Afro pop','Afro pop'),
        ('K-pop','K-pop'),
        ('Reggae','Reggae'),
        
        # Balladesk
        ('RnB','RnB'),
        ('Ballad','Ballad'),
        ('Gospel','Gospel'),

        # Dance
        ('Dance','Dance'),
        ('House music','House music'),
        
        # Classical
        ('Opera','Opera'),
        ('Classical','Classical'),
        ('Soundtrack','Soundtrack'),
        
        # Other
        ('Trance','Trance'),
        ('Lo-fi','Lo-fi'),
        ('New wave','New wave'),
        ('Ambient music','Ambient music'),
        ('World music','World music'),
        ('Folk','Folk'),

        ('Jazz','Jazz'),
    ]

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
    genre = models.CharField(max_length=100, null=False, blank=False, default='Rock', choices=GENRES)
    is_explicit = models.BooleanField(default=False)
    spotify = models.URLField(max_length=200, null=True, blank=True)
    soundcloud = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)
    
    displayed_upvotes = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)