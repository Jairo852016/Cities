# server/cities/serializers.py

from rest_framework import serializers

from .models import Cities


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ('id', 'citie', 'lat', 'lng', 'country', 'iso2', 'admin_name','capital','population','population_proper',)