# server/cities/models.py

import uuid

from django.db import models


class Cities(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    citie = models.CharField(max_length=255)
    lat = models.DecimalField(
        decimal_places=4, max_digits=10, null=True, blank=True
    )
    lng = models.DecimalField(
        decimal_places=4, max_digits=10, null=True, blank=True
    )
    country = models.CharField(max_length=255)
    iso2 = models.CharField(max_length=3)
    admin_name = models.CharField(max_length=255)
    capital= models.CharField(max_length=255)
    population= models.IntegerField()
    population_proper= models.IntegerField()
    

    def __str__(self):
        return f'{self.id}'