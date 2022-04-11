# server/cities/admin.py

from django.contrib import admin

from .models import Cities, CitiesSearchWord
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class CitiesResource(resources.ModelResource):
    class Meta:
        model = Cities


@admin.register(Cities)
class citiesAdmin(ImportExportModelAdmin):
    fields = ('id', 'citie', 'lat', 'lng', 'country', 'iso2', 'admin_name','capital','population','population_proper','search_vector',)
    list_display = ('id', 'citie', 'lat', 'lng', 'country', 'iso2', 'admin_name','capital','population','population_proper',)
    #list_filter = ('citie', 'iso2','capital')
    #ordering = ('citie',)
    #readonly_fields = ('id',)
    resource_class = CitiesResource

@admin.register(CitiesSearchWord)
class citiesSearchWordAdmin(admin.ModelAdmin):
    fields = ('word',)
    list_display = ('word',)
    ordering = ('word',)



