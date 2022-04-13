# server/cities/management/commands/bulk_update.py

from django.core.management.base import BaseCommand

from elasticsearch_dsl import connections
from elasticsearch.helpers import bulk

from cities.constants import ES_INDEX, ES_MAPPING
from cities.models import Cities



class Command(BaseCommand):
    help = 'Updates the Elasticsearch index.'

    def _document_generator(self):
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

    def handle(self, *args, **kwargs):
        self.stdout.write(f'Bulk updating documents on "{ES_INDEX}" index...')
        connection = connections.get_connection()
        succeeded, _ = bulk(connection, actions=self._document_generator(), stats_only=True)
        self.stdout.write(f'Updated {succeeded} documents on "{ES_INDEX}" successfully')

       
