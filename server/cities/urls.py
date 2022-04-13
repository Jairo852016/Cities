# server/cities/urls.py

#Django
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

#Views
from .views import CitiesView, CitiesSearchWordsView, ESCitiesView , ESCitiesSearchWordsView,CitiesPaginationView,CitieListView
from . import views

urlpatterns = [
    path('cities/', ESCitiesView.as_view()),
    path('es-cities/', ESCitiesView.as_view()),
    path('pg-cities/', CitiesView.as_view()), 
    path('pg-citiespag/', CitiesPaginationView.as_view()), 
    path('cities-search-words/',ESCitiesSearchWordsView.as_view() ), 
    path('es-cities-search-words/', ESCitiesSearchWordsView.as_view()),
    path('pg-cities-search-words/', CitiesSearchWordsView.as_view()),
    #path("upload/",views.upload, name="upload"),
    #path("pagination/",CitieListView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


