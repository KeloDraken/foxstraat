from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


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
    has_server = models.BooleanField(default=False)
    gelt = models.PositiveIntegerField(default=1000)
    num_posts = models.PositiveIntegerField(default=0)
    username = LowercaseCharField(
        # Copying this from AbstractUser code
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator(),],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    display_name = models.CharField(max_length=20, null=True, blank=True)
    profile_pic = ProcessedImageField(
        upload_to='accounts/profile_pics/',
        processors=[ResizeToFit(320, 440)],
        format='JPEG',
        options={'quality': 90},
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
    website = models.CharField(max_length=300, null=True, blank=True)
    default_styles = models.TextField(
        null=False, 
        blank=False, 
        default=
        """
<style>
    /* 
    You may edit other HTML Tags' styles.
    
    This Google font is a part of our branding. 
    YOU ARE NOT ALLOWED TO CHANGE THIS FONT */
    @import url("https://fonts.googleapis.com/css2?family=Lobster&display=swap");
    /* Fonts used in this page. You can change these. */
    @import url('https://use.fontawesome.com/releases/v5.0.7/css/all.css');

    /* Branding styles begin */
    .logo {
        /* 
        The logo font size cannot be less than 2em.
        You may change the logo's colours, however, 
        there needs to be ENOUGH CONTRAST between the 
        logo and the background so much that the logo 
        still remains visible. 
        */
        font-size: 2em !important;
        color: #212121;
        padding: 10px 16px;
        text-decoration: none;
        float: left;
        font-family: "Lobster", cursive;
    }

    /* Branding styles end */

    .container {
        /* Add a top margin to avoid content overlay */
        margin: 7rem 7rem;
    }

    /* Navbar styles */
    .navbar {
        overflow: hidden;
        background-color: #fff;
        box-shadow: 0 3px 5px 0 rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(0, 0, 0, 0.08);
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
    }

    .nav-links {
        float: left;
        font-weight: 600;
        font-family: Arial, Helvetica, sans-serif;
        margin-top: 10px;
        display: block;
        color: #212121;
        font-size: 1em;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }

    .nav-links:hover {
        background: #ddd;
        color: black;
    }

    /* Navbar styles end */

    .section-heading {
        font-family: Arial, Helvetica, sans-serif;
        color: #212121;
    }

    /* User basic info styles */
    .user-details-basic-container {
        margin-top: 1rem;
        width: 100%;
    }

    .profile-image-container {
        margin-right: 3rem;
        margin-top: 1rem;
    }

    .profile-picture {
        object-fit: cover;
        width: 240px;
        height: 240px;
    }

    .username-container {
        margin-top: 5px;
    }

    .username {
        margin-bottom: 0;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 1.8em;
        font-weight: 600 !important;
    }

    .user-stat-container {
        margin-top: 5px;
    }

    .stat {
        float: left;
        display: block;
        font-size: 0.9em;
        font-family: Arial, Helvetica, sans-serif;
        color: rgb(155, 155, 155);
        font-weight: 700;
        margin-right: 1em !important;
    }
    .join-btn-container{
        width: 88%;
    }
    .join-btn{
        cursor: pointer;
        border: 0;
        width: 100%;
        border-radius: 2px;
        font-weight: 600;
        font-size: 1.2em;
        color: #fff;
        box-shadow: #4e4e4e 2px 2px 4px;
        padding: 7px;
        background-color: #181818;
    }
    /* user basic info styles end */

    /* user advanced info styles start */
    .user-details-advanced-container {
        width: 100%;
    }

    .social-links-container {
        margin-top: 5px;
    }

    .social-link {
        text-decoration: none;
        color: rgb(118, 118, 134);
        font-weight: 600;
        font-size: 1.2em;
        margin-right: 15px;
    }

    .bio-container {
        margin-top: 2rem;
    }

    .bio {
        font-family: Arial, Helvetica, sans-serif;
        color: #333333;
        font-weight: 500;
        white-space: pre-wrap;
    }

    /* user advanced info styles end */

    /* Post image styles */
    .post-image {
        width: 260px;
        height: 260px;
        margin-bottom: 1.5rem;
        object-fit: cover;
    }
    /* post image styles end */
</style>
    """
    )
    custom_styles = models.TextField(
        null=False, 
        blank=False, 
        default=
        """
<style>
    /* 
    You may edit other HTML Tags' styles.
    
    This Google font is a part of our branding. 
    YOU ARE NOT ALLOWED TO CHANGE THIS FONT */
    @import url("https://fonts.googleapis.com/css2?family=Lobster&display=swap");
    /* Fonts used in this page. You can change these. */
    @import url('https://use.fontawesome.com/releases/v5.0.7/css/all.css');
    
    /* Branding styles begin */
    .logo {
        /* 
        The logo font size cannot be less than 2em.
        You may change the logo's colours, however, 
        there needs to be ENOUGH CONTRAST between the 
        logo and the background so much that the logo 
        still remains visible. 
        */
        font-size: 2em !important;
        color: #212121;
        padding: 10px 16px;
        text-decoration: none;
        float: left;
        font-family: "Lobster", cursive;
    }
    /* Branding styles end */

    .container {
        /* Add a top margin to avoid content overlay */
        margin: 7rem 7rem;
    }

    /* Navbar styles */
    .navbar {
        overflow: hidden;
        background-color: #fff;
        box-shadow: 0 3px 5px 0 rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(0, 0, 0, 0.08);
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
    }
    .nav-links {
        float: left;
        font-weight: 600;
        font-family: Arial, Helvetica, sans-serif;
        margin-top: 10px;
        display: block;
        color: #212121;
        font-size: 1em;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    .nav-links:hover {
        background: #ddd;
        color: black;
    }
    /* Navbar styles end */

    .section-heading {
        font-family: Arial, Helvetica, sans-serif;
        color: #212121;
    }

    /* User basic info styles */
    .user-details-basic-container {
        margin-top: 1rem;
        width: 100%;
    }
    .profile-image-container {
        margin-right: 3rem;
        margin-top: 1rem;
    }
    .profile-picture {
        object-fit: cover;
        width: 240px;
        height: 240px;
    }
    .username-container {
        margin-top: 5px;
    }
    .username {
        margin-bottom: 0;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 1.8em;
        font-weight: 600 !important;
    }
    .user-stat-container {
        margin-top: 5px;
    }
    .stat {
        float: left;
        display: block;
        font-size: 0.9em;
        font-family: Arial, Helvetica, sans-serif;
        color: rgb(155, 155, 155);
        font-weight: 700;
        margin-right: 1em !important;
    }
    /* user basic info styles end */

    /* user advanced info styles start */
    .user-details-advanced-container{
        width: 100%;
    }
    .social-links-container {
        margin-top: 5px;
    }
    .social-link {
        text-decoration: none;
        color: rgb(118, 118, 134);
        font-weight: 600;
        font-size: 1.2em;
        margin-right: 15px;
    }
    .bio-container {
        margin-top: 2rem;
    }
    .bio {
        font-family: Arial, Helvetica, sans-serif;
        color: #333333;
        font-weight: 500;
        white-space: pre-wrap;
    }
    /* user advanced info styles end */

    /* Post image styles */
    .post-image {
        width: 260px;
        height: 260px;
        margin-bottom: 1.5rem;
        object-fit: cover;
    }
    /* post image styles end */
</style>
        """
    )
    date_joined = models.DateField(auto_now_add=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username