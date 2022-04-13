# Celery

from celery import shared_task
import time 

from django.core.management.base import BaseCommand

from elasticsearch_dsl import connections
from elasticsearch.helpers import bulk

from cities.constants import ES_INDEX, ES_MAPPING
from cities.models import Cities

#@task(name='sleep_for', max_retries=3)
@shared_task
def sleep_for():
    for i in  range (50):
        time.sleep(1)
        print("Sleeping", str(i+1))






def _document_generator():
        for citie in Cities.objects.iterator():
             yield {
                '_index': ES_INDEX,
                '_id': citie.id,
                'citie': citie.citie,
                'lat':citie.lat,
                'lng':citie.lng,
                'country' :citie.country,
                'iso2':citie.iso2,
                'admin_name': citie.admin_name,
                'capital':citie.capital,
                'population':citie.population,
                'population_proper':citie.population_proper,
             }

def handle_Elastic():
    #self.stdout.write(f'Bulk updating documents on "{ES_INDEX}" index...')
    connection = connections.get_connection()
    succeeded, _ = bulk(connection, actions=_document_generator(), stats_only=True)
    print("1")
    ##self.stdout.write(f'Updated {succeeded} documents on "{ES_INDEX}" successfully')


