import random
import string

from core.bulletin.models import (
    Bulletin,
    BulletinImage, 
    PostTag, 
    Tag
)


def object_id_generator(size, model, chars=string.ascii_letters + string.digits):
    """
    Generates and returns base64 call id
    """
    object_id = ''.join(random.choice(chars) for _ in range(size))

    return check_object_id_exists(object_id=object_id, model=model)

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


def extract_hashtags(text) -> list:
    """
    function to extract all the hashtags in a product description. 
    It generates new `Tag` instance, if it does not exist, for each of 
    of the tags
    """
      
    # initializing hashtag_list variable
    hashtag_list = []
      
    # splitting the text into words
    for word in text.split():
          
        # checking the first charcter of every word
        if word[0] == '#':
              
            # adding the word to the hashtag_list
            hashtag_list.append(word[1:])
      
    # printing the hashtag_list
    for hashtag in hashtag_list:
            obj, created = Tag.objects.get_or_create(
                name=hashtag.lower(),
            )

    return hashtag_list


def link_tags_to_post(post_id: str, tags: list):
    post  = Bulletin.objects.get(object_id=post_id)
    post_image = BulletinImage.objects.get(bulletin=post)

    for tag in tags:
        _tag = Tag.objects.get(name=tag.lower())
        PostTag.objects.create(post=post_image, tag=_tag)