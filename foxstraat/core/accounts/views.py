from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import Http404

from django.shortcuts import get_object_or_404, redirect, render

from foxstraat.utils.helpers import forbidden_attributes, is_mobile
from foxstraat.core.forms import FormWithCaptcha

from foxstraat.core.accounts.forms import UserLoginForm, UserRegistrationForm
from foxstraat.core.accounts.models import User
from foxstraat.core.announcements.models import Announcement, ProductAnnouncement
from foxstraat.core.bulletin.models import Bulletin


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
        return render(request, "views/frontpage/explore_users.html", context)
    else:
        return redirect("index")


def user_registration(request):
    if not is_mobile(request):
        if request.user.is_authenticated:
            return redirect("accounts:user-dashboard")
        else:
            captcha = FormWithCaptcha

            if request.method == "POST":
                registration_form = UserRegistrationForm(request.POST)

                # TODO: remove this try/catch in production
                # try:
                captcha_data = request.POST["g-recaptcha-response"]
                # except:
                #     captcha_data = '...'

                if not captcha_data == "" and not captcha_data == None:
                    if registration_form.is_valid():
                        registration_form.save()

                        username = request.POST["username"]
                        password = request.POST["password2"]

                        user = authenticate(
                            username=username.lower(), password=password
                        )

                        if user is not None:
                            login(request, user)
                            messages.success(
                                request, "Welcome to Foxstraat. Feel free to explore."
                            )
                            return redirect("accounts:user-dashboard")
                        else:
                            pass
                else:
                    messages.error(request, "Please confirm that you're not a robot")
            else:
                registration_form = UserRegistrationForm()

            context = {
                "registration_form": registration_form,
                "captcha": captcha,
            }
            return render(request, "views/auth/registration_form.html", context)
    else:
        return redirect("index")


class UserLoginView(LoginView):
    template_name = "views/auth/login_form.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


user_login = UserLoginView.as_view()


@login_required
def user_logout(request):
    logout(request)
    return redirect("accounts:user-login")


@login_required
def user_dashboard(request):
    if not is_mobile(request):
        announcements = Announcement.objects.all().order_by("-datetime_created")
        product_announcements = ProductAnnouncement.objects.all().order_by(
            "-datetime_created"
        )
        posts = Bulletin.objects.all().exclude(user=request.user).order_by("?")[:3]
        context = {
            "posts": posts,
            "product_announcements": product_announcements,
            "announcements": announcements,
        }
        return render(request, "views/dashboard/dashboard.html", context)
    else:
        return redirect("index")


def get_user_profile(request, username):
    if not is_mobile(request):
        user = get_object_or_404(User, username=username)

        if user.is_active:
            posts = Bulletin.objects.filter(user=user).order_by("-datetime_created")

            try:
                page_number = int(request.GET.get("sida"))
            except:
                page_number = 1

            paginator = Paginator(posts, 15)
            page_obj = paginator.get_page(page_number)

            context = {"page_obj": page_obj, "user": user}
            return render(request, "views/accounts/user_profile.html", context)
        else:
            raise Http404
    else:
        return redirect("index")


def save_profile(request, custom_styles):
    """
    Continues to save other fields in Edit Profile
    """
    user = request.user

    if request.FILES.get("profile_pic"):
        user.profile_pic = request.FILES.get("profile_pic")

    bio = request.POST["about_me"]

    if len(bio) > 220:
        messages.error(
            request, "Your bio is too long. Please keep it at 220 characters of less"
        )
    else:
        user.bio = bio

    is_artist = request.POST.get("is_artist")
    if is_artist == "on":
        user.is_artist = True
    else:
        pass

    is_blogger = request.POST.get("is_blogger")
    if is_blogger == "on":
        user.is_blogger = True
    else:
        pass

    display_name = request.POST["display_name"]
    if not len(display_name) <= 0 and not display_name == None:
        user.display_name = display_name
    else:
        pass

    instagram = request.POST["instagram"]
    if not len(instagram) <= 0 and not instagram == None:
        user.instagram = instagram
    else:
        user.instagram = None

    twitter = request.POST["twitter"]
    if not len(twitter) <= 0 and not twitter == None:
        user.twitter = twitter
    else:
        user.twitter = None

    website = request.POST["website"]
    if not len(website) <= 0 and not website == None:
        user.website = website
    else:
        user.website = None

    if not len(custom_styles) <= 0 and not custom_styles == None:
        user.custom_styles = custom_styles
    else:
        user.custom_styles = None

    user.save()
    messages.success(request, "Profile successfully updated")


@login_required
def edit_user_profile(request):
    if request.method == "POST":
        custom_styles = request.POST["custom_styles"]

        forbidden = forbidden_attributes()
        for i in forbidden:
            if i in custom_styles.lower():
                context = {
                    "user": request.user,
                }
                messages.error(
                    request,
                    """
                    Only css is allowed.
                    Continued use of non-css code could result 
                    in a permanent ban from Foxstraat.
                    """,
                )
                return render(request, "views/accounts/edit_profile.html", context)

        save_profile(request, custom_styles)

    context = {
        "user": request.user,
    }
    return render(request, "views/accounts/edit_profile.html", context)


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
