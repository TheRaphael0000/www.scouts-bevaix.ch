from django.urls import path

from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('scoutisme', views.scoutisme, name='scoutisme'),
    path('actualites', views.actualites, name='actualites'),
    path('calendrier', views.calendrier, name='calendrier'),
    path('albums', views.albums, name='albums'),
    path('locations', views.locations, name='locations'),
    path('carte', views.carte, name='carte'),
    path('contacts', views.contacts, name='contacts'),
]
