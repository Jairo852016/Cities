# server/cities/filter.py

from django.db.models import Q

from django_filters.rest_framework import CharFilter, FilterSet

from .models import Cities

#Este código transcribe los parámetros de cadena de consulta en consultas SQL a través de Django ORM.
class CitiesFilterSet(FilterSet):
    query = CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        search_query = Q(
            Q(citie__contains=value) |
            Q(admin_name__contains=value)
        )
        return queryset.filter(search_query)

    class Meta:
        model = Cities
        fields = ('query', 'country', 'capital',)