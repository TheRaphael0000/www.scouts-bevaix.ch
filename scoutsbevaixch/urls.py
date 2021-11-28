from django.urls import path

from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('scoutisme', views.scoutisme, name='scoutisme'),
    path('actualites', views.actualites, name='actualites'),
    path('calendrier', views.calendrier, name='calendrier'),

    path('albums', views.albums, name='albums'),
    path('albums/<str:name>', views.albums, name='albums'),
    path('image/<str:album>/<str:name>', views.image, name='image'),
    path('thumbnail/<str:album>/<str:name>',
         views.thumbnail, name='thumbnail'),

    path('locations', views.locations, name='locations'),
    path('carte', views.carte, name='carte'),
    path('contacts', views.contacts, name='contacts'),
]
