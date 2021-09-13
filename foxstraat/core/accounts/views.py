from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import Http404

from django.shortcuts import get_object_or_404, redirect, render

from foxstraat.utils.helpers import is_mobile
from foxstraat.core.forms import FormWithCaptcha

from foxstraat.core.accounts.forms import UserLoginForm, UserRegistrationForm
from foxstraat.core.accounts.models import User
from foxstraat.core.posts.models import Post


def explore_users(request):
    user_objects = User.objects.all().order_by("-datetime_joined")
    paginator = Paginator(user_objects, 20)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    if not is_mobile(request):
        context = {"heading": "Cool new people", "page_obj": page_obj}
        return render(request, "public/frontpage/explore_users.html", context)
    else:
        return redirect("index")


def check_captcha(request):
    """
    Checks if request object has valid captcha
    """
    captcha_data = request.POST["g-recaptcha-response"]
    if not captcha_data == "" and not captcha_data == None:
        return True
    return False


def login_user_on_register(request):
    """
    Logs user in on successful `User` instance creation
    """
    username = request.POST["username"]
    password = request.POST["password2"]

    user = authenticate(username=username.lower(), password=password)

    if user is not None:
        login(request, user)
        messages.success(request, "Welcome to Foxstraat. Feel free to explore.")
        return redirect("accounts:user-dashboard")
    else:
        messages.error(request, "Something went wrong")


def user_registration(request):
    if not is_mobile(request):
        if request.user.is_authenticated:
            return redirect("accounts:user-dashboard")
        else:
            captcha = FormWithCaptcha

            if request.method == "POST":
                registration_form = UserRegistrationForm(request.POST)

                if registration_form.is_valid():
                    registration_form.save()

                    return login_user_on_register(request)
            else:
                registration_form = UserRegistrationForm()

            context = {
                "registration_form": registration_form,
                "captcha": captcha,
            }
            return render(request, "public/auth/registration_form.html", context)
    else:
        return redirect("index")


class UserLoginView(LoginView):
    template_name = "public/auth/login_form.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


user_login = UserLoginView.as_view()


@login_required
def user_logout(request):
    logout(request)
    return redirect("accounts:user-login")


def get_user_profile(request, username):
    if not is_mobile(request):
        user = get_object_or_404(User, username=username)

        if user.is_active:
            posts = Post.objects.filter(user=user).order_by("-datetime_created")

            try:
                page_number = int(request.GET.get("sida"))
            except:
                page_number = 1

            paginator = Paginator(posts, 15)
            page_obj = paginator.get_page(page_number)

            context = {"page_obj": page_obj, "user": user}
            return render(request, "public/accounts/user_profile.html", context)
        else:
            raise Http404
    else:
        return redirect("index")


def change_web_url(user, website):
    if not len(website) <= 0 and not website == None:
        user.website = website
    else:
        user.website = None


def change_twitter_handle(user, twitter):
    if not len(twitter) <= 0 and not twitter == None:
        user.twitter = twitter
    else:
        user.twitter = None


def change_instagram_handle(user, instagram):
    if not len(instagram) <= 0 and not instagram == None:
        user.instagram = instagram
    else:
        user.instagram = None


def change_display_name(user, display_name):
    if not len(display_name) <= 0 and not display_name == None:
        user.display_name = display_name
    else:
        pass


def change_bio(request, user, bio):
    if len(bio) > 220:
        messages.error(
            request, "Your bio is too long. Please keep it at 220 characters of less"
        )
    else:
        user.bio = bio


def update_profile_pic(request, user):
    if request.FILES.get("profile_pic"):
        user.profile_pic = request.FILES.get("profile_pic")


def save_profile(request, custom_styles):
    """
    Continues to save other fields in Edit Profile
    """
    user = request.user

    update_profile_pic(request, user)

    bio = request.POST["about_me"]

    change_bio(request, user, bio)

    display_name = request.POST["display_name"]
    change_display_name(user, display_name)

    instagram = request.POST["instagram"]
    change_instagram_handle(user, instagram)

    twitter = request.POST["twitter"]
    change_twitter_handle(user, twitter)

    website = request.POST["website"]
    change_web_url(user, website)

    user.save()
    messages.success(request, "Profile successfully updated")


@login_required
def edit_user_profile(request):
    if request.method == "POST":
        return save_profile(request)

    context = {
        "user": request.user,
    }
    return render(request, "private/accounts/edit_profile.html", context)


@login_required
def delete_account(request):
    if request.user.is_superuser:
        messages.error(
            request, "Admins need to use the admin site to delete their accounts"
        )
        return redirect("accounts:user-dashboard")
    else:
        messages.success(request, "You account has been deleted")
        request.user.is_active = False
        request.user.save()
        return user_logout(request)
