from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class Template(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    name = models.CharField(max_length=140, null=False, blank=False)
    description = models.CharField(max_length=280, null=False, blank=False)
    screenshot_1 = ProcessedImageField(
        upload_to='marketplace/templates/',
        processors=[ResizeToFit(480, 600)],
        format='JPEG',
        options={'quality': 90},
        null=False,
        blank=False,
    )
    screenshot_2 = ProcessedImageField(
        upload_to='marketplace/templates/',
        processors=[ResizeToFit(480, 600)],
        format='JPEG',
        options={'quality': 90},
        null=False,
        blank=False,
    )
    price = models.PositiveIntegerField(default=0)
    template = models.TextField(null=False, blank=False)