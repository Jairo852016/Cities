# server/cities/serializers.py

#Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Models
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


"""class CreateCitiesSerializar(serializers.Serializer):
    Create cities serializar

    citie=serializers.CharField(
        max_length=255,
        validators=[
            UniqueValidator(queryset=Cities.objects.all())
        ]
    )
    lat = serializers.DecimalField(decimal_places=4,max_digits=10)
    lng=serializers.DecimalField(decimal_places=4,max_digits=10)
    country=serializers.CharField(max_length=255)
    iso2=serializers.CharField(max_length=3)
    admin_name=serializers.CharField(max_length=255)
    capital=serializers.CharField(max_length=255) 
    population=serializers.DecimalField(decimal_places=2,max_digits=10)
    population_proper=serializers.DecimalField(decimal_places=2,max_digits=10)

    def create(self, data):
        return Cities.objects.create(**data)"""
