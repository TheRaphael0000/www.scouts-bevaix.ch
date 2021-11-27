from django.shortcuts import render


def albums(request):
    return render(request, "albums.html")
