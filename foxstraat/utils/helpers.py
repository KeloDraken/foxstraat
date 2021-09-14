import random
import re
import string

from foxstraat.core.posts.models import Post


def is_mobile(request):
    """
    returns True if request comes from mobile device
    """
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META.get("HTTP_USER_AGENT")):
        return True
    else:
        return False


def object_id_generator(size, model, chars=string.ascii_letters + string.digits):
    """
    Generates and returns base64 call id
    """
    object_id = "".join(random.choice(chars) for _ in range(size))

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
