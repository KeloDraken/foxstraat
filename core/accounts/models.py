from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    object_id = models.CharField(max_length=20, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)
    custom_styles = models.TextField(
        null=False, 
        blank=False, 
        default=
        """
            <style>
                /* 
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

                    /* Set the navbar to f ixed position */
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

                /* Main content */
                .main {
                    /* Add a top margin to avoid content overlay */
                    margin-top: 30px;
                }
            </style>
        """
    )

    def __str__(self) -> str:
        return self.username