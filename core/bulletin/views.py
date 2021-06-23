from django.shortcuts import render


def create_bulletin(request):
    return render(request, 'bulletin/create_bulletin.html')