# server/cities/management/commands/elasticsearch.py

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
        connection = connections.get_connection()

        self.stdout.write(f'Checking if index "{ES_INDEX}" exists...')
        if connection.indices.exists(index=ES_INDEX):
            self.stdout.write(f'Index "{ES_INDEX}" already exists')
            self.stdout.write(f'Updating mapping on "{ES_INDEX}" index...')
            connection.indices.put_mapping(index=ES_INDEX, body=ES_MAPPING)
            self.stdout.write(f'Updated mapping on "{ES_INDEX}" successfully')
        else:
            self.stdout.write(f'Index "{ES_INDEX}" does not exist')
            self.stdout.write(f'Creating index "{ES_INDEX}"...')
            connection.indices.create(index=ES_INDEX, body={
                'settings': {
                    'number_of_shards': 1,
                    'number_of_replicas': 0,
                     "analysis": {
                        "filter" : {
                            "default_spanish_stemmer" : {
                                "type" : "stemmer",
                                "name" : "spanish"
                            },
                            "default_spanish_stopwords": {
                                "type":        "stop",
                                "stopwords": [ "_spanish_" ]
                            }
                        },
                        
                        "analyzer":{
                            "mianalizador": {
                                "tokenizer": "standard",
                                "filter":  [ "lowercase", "asciifolding", "default_spanish_stopwords", "default_spanish_stemmer" ]
                            }
                        }
                    }
	
                },
                'mappings': ES_MAPPING,
            })
            self.stdout.write(f'Index "{ES_INDEX}" created successfully')

        self.stdout.write(f'Bulk updating documents on "{ES_INDEX}" index...')
        succeeded, _ = bulk(connection, actions=self._document_generator(), stats_only=True)
        self.stdout.write(f'Updated {succeeded} documents on "{ES_INDEX}" successfully')
