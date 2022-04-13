# server/cities/filter.py

#Django
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import CharField, F, Func, Q, TextField, Value

#Django REST Framework
from django_filters.rest_framework import CharFilter, FilterSet

#Models
from .models import Cities, CitiesSearchWord

#Este código transcribe los parámetros de cadena de consulta en consultas SQL a través de Django ORM.
class CitiesFilterSet(FilterSet):
    query = CharFilter(method='filter_query')

    #def filter_query(self, queryset, name, value):
    #    search_query = Q(
    #        Q(citie__contains=value) |
    #        Q(admin_name__contains=value)
    #    )
    #       return queryset.filter(search_query)

    #
    #def filter_query(self, queryset, name, value):
    #    search_query = Q(
    #        Q(citie__search=value) |
    #        Q(admin_name__search=value) 
    #    )
    #    return queryset.filter(search_query)
    
    
    #def filter_query(self, queryset, name, value):
    #    search_query = Q(
    #        Q(search_vector=SearchQuery(value))
    #    )
    #    return queryset.annotate(
    #        search_rank=SearchRank(F('search_vector'), SearchQuery(value))
    #    ).filter(search_query).order_by('-search_rank', 'id')
    
    #def filter_query(self, queryset, name, value):
    #    search_query = Q(
    #        Q(search_vector=SearchQuery(value))
    #    )
    #    return queryset.annotate(
    #        variety_headline=SearchHeadline(F('variety'), SearchQuery(value)),
    #        winery_headline=SearchHeadline(F('winery'), SearchQuery(value)),
    #        description_headline=SearchHeadline(F('description'), SearchQuery(value)),
    #        search_rank=SearchRank(F('search_vector'), SearchQuery(value))
    #    ).filter(search_query).order_by('-search_rank', 'id')

    def filter_query(self, queryset, name, value):
        return queryset.search(value)


    class Meta:
        model = Cities
        fields = ('query', 'country', 'capital',)

class CitiesSearchWordFilterSet(FilterSet):
    query = CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        return queryset.search(value)

    class Meta:
        model = CitiesSearchWord
        fields = ('query',)

