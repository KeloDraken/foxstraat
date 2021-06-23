from django.shortcuts import redirect, render

from utils.helpers import object_id_generator

from core.bulletin.models import Bulletin


def create_bulletin(request):
    if not request.user.is_authenticated:
        return redirect('accounts:user-login')
    else:
        user = request.user
        object_id = object_id_generator(11, Bulletin)

        if request.method == 'POST':
            caption = request.POST['caption']
            new_bulletin = Bulletin.objects.create(
                user=user,
                object_id=object_id,
                caption=caption
            )
            new_bulletin.save()
            return redirect('/')
        return render(request, 'bulletin/create_bulletin.html')

