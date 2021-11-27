from django.shortcuts import render
from .contacts_data import contacts as c


def contacts(request):
    return render(request, "contacts.html", context={"contacts": c})
