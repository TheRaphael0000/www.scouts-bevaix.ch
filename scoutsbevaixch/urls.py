from django.urls import path

from . import views

urlpatterns = [
    path(r'accueil', views.accueil, name='accueil'),
    path(r'', views.accueil, name='accueil'),

    path('login', views.login, name='login'),
    path('logoff', views.logoff, name='logoff'),
    path('log', views.log, name='log'),

    path('scoutisme', views.scoutisme, name='scoutisme'),
    path('actualites', views.actualites, name='actualites'),
    path('calendrier', views.calendrier, name='calendrier'),

    path('albums', views.albums, name='albums'),
    path('albums/<str:name>', views.albums_name, name='albums'),
    path('image/<str:album>/<str:privacy>/<str:name>', views.image, name='image'),
    path('thumbnail/<str:album>/<str:privacy>/<str:name>',
         views.thumbnail, name='thumbnail'),

    path('locations', views.locations, name='locations'),
    path('reservations', views.Reservations.as_view(), name='reservations'),
    path('validation/<str:id>', views.validation, name='validation'),
    path('reservations_confirmation', views.reservations_confirmation,
         name='reservations_confirmation'),
    path('emplacement', views.emplacement, name='emplacement'),
    path('contacts', views.contacts, name='contacts'),
]
