from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from core.accounts.models import User


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
        null=True,
        blank=True
    )
    artists = models.CharField(max_length=1000, null=True, blank=True)
    genre = models.CharField(max_length=100, null=False, blank=False, default='Rock', choices=GENRES)
    is_explicit = models.BooleanField(default=False, null=True)
    spotify = models.URLField(max_length=200, null=True, blank=True)
    soundcloud = models.URLField(max_length=200, null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)
    
    score = models.IntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class VoteSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    bulletin = models.ForeignKey(Song, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    has_voted = models.BooleanField(default=False)
   