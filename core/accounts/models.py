from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    object_id = models.CharField(max_length=20, null=True, blank=True)

    bio = models.TextField(null=True, blank=True, max_length=3000)

    # User social media links
    instagram = models.CharField(max_length=60, null=True, blank=True)
    twitter = models.CharField(max_length=60, null=True, blank=True)
    youtube = models.CharField(max_length=60, null=True, blank=True)
    twitch = models.CharField(max_length=60, null=True, blank=True)
    tiktok = models.CharField(max_length=60, null=True, blank=True)
    github = models.CharField(max_length=60, null=True, blank=True)
    vsco = models.CharField(max_length=60, null=True, blank=True)
    dribbble = models.CharField(max_length=60, null=True, blank=True)
    
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

    def __str__(self) -> str:
        return self.username