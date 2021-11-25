from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template.loader import get_template
from .contacts import contacts as c

def accueil(request):
    return render(request, "accueil.html")


def scoutisme(request):
    return render(request, "scoutisme.html")


def actualites(request):
    return render(request, "actualites.html")


def calendrier(request):
    return render(request, "calendrier.html")


def albums(request):
    return render(request, "albums.html")


def locations(request):
    return render(request, "locations.html")


def carte(request):
    return render(request, "carte.html")


def contacts(request):
    return render(request, "contacts.html", context={"contacts": c})
