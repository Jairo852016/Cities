# server/cities/urls.py

from django.urls import path

from .views import CitiesView, CitiesSearchWordsView, ESCitiesView , ESCitiesSearchWordsView, ImportView

urlpatterns = [
    path('cities/', ESCitiesView.as_view()),
    path('es-cities/', ESCitiesView.as_view()),
    path('pg-cities/', CitiesView.as_view()), 
    path('cities-search-words/',ESCitiesSearchWordsView.as_view() ), 
    path('es-cities-search-words/', ESCitiesSearchWordsView.as_view()),
    path('pg-cities-search-words/', CitiesSearchWordsView.as_view()),
    path('import/', ImportView.as_view()),

]