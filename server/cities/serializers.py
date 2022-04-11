# server/cities/serializers.py

from rest_framework import serializers

from .models import Cities, CitiesSearchWord


class CitiesSerializer(serializers.ModelSerializer):
    citie = serializers.SerializerMethodField()
    admin_name = serializers.SerializerMethodField()
    

    
    def get_citie(self, obj):
        if hasattr(obj, 'citie_headline'):
            return getattr(obj, 'citie_headline')
        return getattr(obj, 'citie')

    
    def get_admin_name(self, obj):
        if hasattr(obj, 'admin_name_headline'):
            return getattr(obj, 'admin_name_headline')
        return getattr(obj, 'admin_name')

    class Meta:
        model = Cities
        fields = ('id', 'citie', 'lat', 'lng', 'country', 'iso2', 'admin_name','capital','population','population_proper',)

class CitiesSearchWordSerializer(serializers.ModelSerializer): 
    class Meta:
        model = CitiesSearchWord
        fields = ('word',)