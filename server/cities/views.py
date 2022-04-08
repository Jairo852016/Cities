# server/cities/views.py

from rest_framework.generics import ListAPIView

from .models import Cities
from .serializers import CitiesSerializer
from .filter import CitiesFilterSet


class CitiesView(ListAPIView):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer
    filterset_class = CitiesFilterSet