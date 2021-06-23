from django.shortcuts import redirect, render


def create_bulletin(request):
    if not request.user.is_authenticated:
        return redirect('accounts:user-login')
    else:
        return render(request, 'bulletin/create_bulletin.html')