# server/cities/admin.py

from django.contrib import admin

from .models import Cities


@admin.register(Cities)
class citiesAdmin(admin.ModelAdmin):
    fields = ('id', 'citie', 'lat', 'lng', 'country', 'iso2', 'admin_name','capital','population','population_proper',)
    list_display = ('id', 'citie', 'lat', 'lng', 'country', 'iso2', 'admin_name','capital','population','population_proper',)
    list_filter = ('citie', 'iso2','capital')
    ordering = ('citie',)
    readonly_fields = ('id',)
