from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from foxstraat.core.accounts.validators import UnicodeUsernameValidator


class LowercaseCharField(models.CharField):
    """
    Override CharField to convert to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert text to lowercase.
        """
        value = super(LowercaseCharField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class User(AbstractUser):
    object_id = models.CharField(max_length=20, null=True, blank=True)
    is_fake_profile = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    gelt = models.IntegerField(default=500)
    num_posts = models.PositiveIntegerField(default=0)
    email = LowercaseCharField(
        # Copying this from AbstractUser code
        _("email address"),
        max_length=300,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            UnicodeUsernameValidator(),
        ],
        error_messages={
            "unique": _("This email address already has an account associated with it"),
        },
    )
    display_name = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = ProcessedImageField(
        upload_to="accounts/profile_pics/",
        processors=[ResizeToFit(320, 440)],
        format="JPEG",
        options={"quality": 90},
        null=True,
        blank=True,
    )
    bio = models.TextField(null=True, blank=True, max_length=3000)
    subscribers = models.PositiveBigIntegerField(default=1)
    upvotes = models.PositiveBigIntegerField(default=0)
    # User social media links
    instagram = models.CharField(max_length=60, null=True, blank=True)
    vsco = models.CharField(max_length=60, null=True, blank=True)
    twitter = models.CharField(max_length=60, null=True, blank=True)
    website = models.URLField(max_length=300, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)
