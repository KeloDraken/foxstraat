import random

import requests
from requests.exceptions import ConnectionError

import string


from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect

from bs4 import BeautifulSoup

from foxstraat.core.models import ForbiddenWebsites
from foxstraat.core.posts.models import Post


def object_id_generator(size, model, chars=string.ascii_letters + string.digits):
    """
    Generates and returns base64 call id
    """
    object_id = "".join(random.choice(chars) for _ in range(size))
    return check_object_id_exists(object_id=object_id, model=model)


def is_forbidden(url):
    forbidden_sites = ForbiddenWebsites.objects.all()

    if not url == None and len(url) > 0:
        for i in forbidden_sites:
            if url in i.domain:
                return True
            else:
                return False
    else:
        return True


def add_post_to_db(url, publisher, title, description, image, request=None):
    """
    Commits page data to db, creating new `Post` object
    """
    object_id = object_id_generator(size=11, model=Post)
    try:
        is_forbidden_site = is_forbidden(url)

        if not is_forbidden_site:
            messages.error(
                request,
                "Link wasn't added because the host has been banned from Foxstraat",
            )
            return redirect("posts:create-post")

        else:
            post = Post.objects.create(
                object_id=object_id,
                user=request.user,
                url=url,
                publisher=publisher,
                title=title,
                description=description,
                image=image,
            )
    except IntegrityError:
        messages.error(
            request,
            "Couldn't create submission because the page is missing important information",
        )
        return redirect("posts:create-post")

    return redirect("posts:get-post", post_id=object_id)


def extract_page_data(url, request=None):
    """
    Extracts page information using Open Graph protocol
    """
    # try:
    try:
        src = requests.get(url)
    except ConnectionError:
        messages.error(request, "Couldn't connect to website")
        return redirect("posts:create-post")

    soup = BeautifulSoup(src.text, "lxml")

    og_title = soup.find("meta", property="og:title")
    og_url = soup.find("meta", property="og:url")
    og_site_name = soup.find("meta", property="og:site_name")
    og_image = soup.find("meta", property="og:image")
    og_description = soup.find("meta", property="og:description")
    yt_channel_name = soup.find("link", itemprop="name")

    if not og_title == None:
        title = og_title["content"]
    else:
        title = None

    if not og_url == None:
        recipe_link = og_url["content"]
    else:
        recipe_link = None

    if not og_site_name == None:
        site_name = og_site_name["content"]
    else:
        site_name = "Foxstraat"

    if not og_image == None:
        cover_image = og_image["content"]
    else:
        cover_image = None

    if not og_description == None:
        description = og_description["content"]
    else:
        description = None

    if not yt_channel_name == None:
        site_name = yt_channel_name["content"]
    else:
        pass

    return add_post_to_db(
        url=recipe_link,
        publisher=site_name,
        title=title,
        description=description,
        image=cover_image,
        request=request,
    )


def check_object_id_exists(object_id, model):
    """
    Checks if call id exists. Generates and returns new call id if exists
    """
    # Try/Catch checks to see if a Submission with object_id == object_id
    # already exists. This will not throw an error if True. And if
    # that's the case, the function becomes recursive until a unique
    # object_id is generated
    try:
        model.objects.get(object_id=object_id)

        # New object_id generated
        new_object_id = object_id_generator()

        # New object_id checked against all Submission objects
        check_object_id_exists(object_id=new_object_id, model=model)

    except:
        # This means there has been an error which means
        # that there's no Submission object with object_id == object_id
        return object_id
