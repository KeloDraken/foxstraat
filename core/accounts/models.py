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
    is_verified = models.BooleanField(default=False)
    profile_pic = ProcessedImageField(
        upload_to='accounts/profile_pics/',
        processors=[ResizeToFit(220, 340)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )

    bio = models.TextField(null=True, blank=True, max_length=3000)

    # User social media links
    instagram = models.CharField(max_length=60, null=True, blank=True)
    vsco = models.CharField(max_length=60, null=True, blank=True)
    website = models.CharField(max_length=300, null=True, blank=True)
    
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

            /* 
            The logo font size cannot be less than 2em.
            You may change the logo's colours, however, there needs to be ENOUGH CONTRAST 
            between the logo and the background so much that the logo still remains visible. 
            */

            /* Branding styles begin */
            .logo {
                font-size: 2em !important;
                color: #fff;
                padding: 10px 16px;
                text-decoration: none;
                float: left;
                font-family: "Lobster", cursive;
            }
            /* Branding styles end */

            /* Navbar styles */
            .navbar {
                overflow: hidden;
                background-color: #333;

                /* Set the navbar to fixed position */
                position: fixed;

                /* Position the navbar at the top of the page */
                top: 0;
                left: 0;

                /* Full width */
                width: 100%;
            }

            /* Links inside the navbar */
            .nav-links {
                float: left;
                margin-top: 10px;
                display: block;
                color: #f2f2f2;
                font-size: 1em;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
            }

            /* Change nav link background colour on mouse-over */
            .nav-links:hover {
                background: #ddd;
                color: black;
            }
            /* Navbar styles end */

            .container {
                /* Add a top margin to avoid content overlay */
                margin: 7rem 5rem;
            }

            /* User basic info styles */
            .user-details-basic-container {
                border: 2px solid #000;
            }
            .profile-image-container {}
            .profile-picture {
                float: left;
                display: block;
                margin-right: 3rem;
                margin-top: 1rem;
            }
            .username-container {}
            .username {
                font-size: 1.5em;
                font-weight: 700;
            }
            .social-links-container {}
            .social-link {
                text-decoration: underline;
                color: blue;
                font-weight: 600;
                margin-right: 5px;
            }        
            .instagram {}        
            .facebook {}        
            .twitter {}        
            .youtube {}
            .twitch {}
            /* user basic info styles end */
            
            /* user advanced info styles start */
            .section-heading{
                color: #000;
            }
            .user-details-advanced-container {
                border: 2px solid #000;
            }
            .user-stat-container {}
            .stat {
                float: left;
                display: block;
                font-size: 1em;
                font-weight: 700;
                margin-right: 1em !important;
            }
            .bio-container{}
            .bio{
                font-family: 'Times New Roman', Times, serif;
                white-space: pre-wrap;
            }
            /* user advanced info styles end */
        </style>
        """
    )

    date_joined = models.DateField(auto_now_add=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)

    # objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username