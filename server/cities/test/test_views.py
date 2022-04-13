# server/cities/tests/test_views.py

#Django
from django.contrib.postgres.search import SearchVector
from django.conf import settings 

#Models
from cities.models import Cities, CitiesSearchWord

#Serializer
from cities.serializers import CitiesSerializer 

#Mapping
from cities.constants import ES_MAPPING

#Elasticsearch
from elasticsearch_dsl import connections
from rest_framework.test import APIClient, APITestCase

#Json, patlib, uuid
import json 
import pathlib 
import uuid 

#Test
from unittest.mock import patch



class ViewTests(APITestCase):
    fixtures = ['test_citie.json']
    
    def setUp(self):
        Cities.objects.all().update(search_vector=(
        SearchVector('citie', weight='A') +
        SearchVector('admin_name', weight='B')
        ))
      
        self.client = APIClient()

    
    def test_empty_query_returns_everything(self):
        response = self.client.get('/api/v1/cities/pg-cities/')
        cities = Cities.objects.all()
        self.assertJSONEqual(response.content, CitiesSerializer(cities, many=True).data)

#Test Query citie
#prueba que dos secuencias de elementos citie contienen los mismos valores en cualquier orden
    
    def test_query_matches_citie(self):
       # response = self.client.get('/api/v1/cities/cities/?query=Bogota')
       # self.assertEquals(1, len(response.data))
       # self.assertEquals("4bef57b7-7dc1-41ae-9f41-027ead4de652", response.data[0]['id'])
        response = self.client.get('/api/v1/cities/pg-cities/?query=Bogota')
        self.assertEquals(2, len(response.data))
        self.assertCountEqual([
        "4bef57b7-7dc1-41ae-9f41-027ead4de652",
        "4b3337b7-7dc1-41ae-9f41-027ead4de652",
        ], [item['id'] for item in response.data])
    
#Test Query admin_name
#Prueba que una secuencias de elementos admin_name contienen los mismos valores en cualquier orden
    def test_query_matches_admin_name(self):
        response = self.client.get('/api/v1/cities/pg-cities/?query=Antioquia')
        self.assertEquals(2, len(response.data))
        self.assertCountEqual([
        "21e40285-cec8-417c-9a26-12a348b7fa3a",
        "444337b7-7dc1-41ae-9f41-027ead4de652",
        ], [item['id'] for item in response.data])
        #self.assertEquals("21e40285-cec8-417c-9a26-12a348b7fa3a", response.data[0]['id'])

#Test Query country

    def test_can_filter_on_country(self):
        response = self.client.get('/api/v1/cities/pg-cities/?country=Colombia')
        self.assertEquals(1, len(response.data))
        self.assertEquals("444337b7-7dc1-41ae-9f41-027ead4de652", response.data[0]['id'])

#Test Query capital

    def test_can_filter_on_capital(self):
        response = self.client.get('/api/v1/cities/pg-cities/?capital=admin')
        self.assertEquals(1, len(response.data))
        self.assertEquals("444337b7-7dc1-41ae-9f41-027ead4de652", response.data[0]['id'])

#Test Query Exact Match cities
#para demostrar que los parámetros de consulta que filtran requieren coincidencias exactas

    def test_cities_must_be_exact_match(self):
        response = self.client.get('/api/v1/cities/pg-cities/?query=Bogotas1')
        self.assertEquals(0, len(response.data))
        self.assertJSONEqual(response.content, [])


#Test Query Search Vector
#ecalcular el search_vectorcada vez que se guarda un registro.
    def test_search_vector_populated_on_save(self):
        citie = Cities.objects.create(
            
            citie = "Barranquilla",
            lat = "4.6126",
            lng = "-74.0705",
            country = "Colombia1",
            iso2 = "CO",
            admin_name = "Atlántico", 
            capital = "primary",
            population= 9464000,
            population_proper = 7963000
        )
        citie = Cities.objects.get(id=citie.id)
        self.assertEqual("'atlántico':2B 'barranquilla':1A", citie.search_vector)

#Resaltando palabra de busqueda
    def test_citie_highlights_matched_words(self):
        response = self.client.get('/api/v1/cities/pg-cities/?query=dos')
        self.assertEquals('Antioquia <mark>dos</mark> tres cuatro', response.data[0]['admin_name'])


#Test Cities Search Word in table cities_citiessearch(word)
    def test_cities_search_words_populated_on_save(self):
        CitiesSearchWord.objects.all().delete()
        Cities.objects.create(
            
            citie = "Barranquilla Colombia",
            lat = "4.6126",
            lng = "-74.0705",
            country = "Colombia1",
            iso2 = "CO",
            admin_name = "Atlántico Jairo prueba", 
            capital = "primary",
            population= 9464000,
            population_proper = 7963000
        )
        cities_search_words = CitiesSearchWord.objects.all().order_by('word').values_list('word', flat=True)
        self.assertListEqual([
            'atlántico',
            'barranquilla',
            'colombia',
            'jairo',
            'prueba'
            
        ], list(cities_search_words))


#Test Word in cities_citiessearch(word) suggests

    def test_suggests_words_for_spelling_mistakes(self):
        CitiesSearchWord.objects.bulk_create([
            #CitiesSearchWord(word='bogota1'),
            #CitiesSearchWord(word='antioquia4'),
            CitiesSearchWord(word='Quito'),
            CitiesSearchWord(word='Guayaquil'),
        ])
        response = self.client.get('/api/v1/cities/pg-cities-search-words/?query=yaquil')
        self.assertEqual(1, len(response.data))
        self.assertEqual('Guayaquil', response.data[0]['word'])


        
class ESViewTests(APITestCase):
    def setUp(self):
        self.index = f'test-cities-{uuid.uuid4()}'
        self.connection = connections.get_connection()
        self.connection.indices.create(index=self.index, body={
            'settings': {
                    'number_of_shards': 1,
                    'number_of_replicas': 0,
                    "analysis": {
                        "analyzer":{
                            "mianalizador": {
                                "tokenizer": "standard",
                                "filter":  [ "lowercase", "asciifolding", "default_spanish_stopwords", "default_spanish_stemmer" ]
                            }
                        },
                        "filter" : {
                            "default_spanish_stemmer" : {
                                "type" : "stemmer",
                                "name" : "spanish"
                            },
                            "default_spanish_stopwords": {
                                "type":        "stop",
                                "stopwords": [ "_spanish_" ]
                            }
                        }
                    }
                },
           'mappings': ES_MAPPING,
        })

        # Load fixture data
        
        fixture_path = pathlib.Path(settings.BASE_DIR / 'cities' / 'fixtures' / 'test_citie.json')
        with open(fixture_path, 'rt') as fixture_file:
            fixture_data = json.loads(fixture_file.read())
            for citie in fixture_data:
                fields = citie['fields']
                self.connection.create(index=self.index, id=fields['id'], body={
                    'citie': fields['citie'],
                    'lat': fields['lat'],
                    'lng':fields['lng'],
                    'country':fields['country'],
                    'iso2':fields['iso2'],
                    'admin_name': fields['admin_name'],
                    'capital':fields['capital'],
                    'population':fields['population'],
                    'population_proper':fields['population_proper'],
                }, refresh=True)
         # Start patching
        self.mock_constants = patch('cities.views.constants').start()
        self.mock_constants.ES_INDEX = self.index
#Test Match citie or admin_name    
    def test_query_matches_citie(self):
        
        response = self.client.get('/api/v1/cities/es-cities/?query=Antioquia')
        #print(response.data)
        self.assertEquals(2, len(response.data))
        self.assertEquals("21e40285-cec8-417c-9a26-12a348b7fa3a", response.data[0]['id'])
    
#Test Result Correct order
    def test_search_results_returned_in_correct_order(self):
        response = self.client.get('/api/v1/cities/es-cities/?query=Bogota')
        self.assertEquals(2, len(response.data))
        self.assertListEqual([
            "4bef57b7-7dc1-41ae-9f41-027ead4de652",
            "4b3337b7-7dc1-41ae-9f41-027ead4de652",
        ], [item['id'] for item in response.data])

#Test match words in admin_name highlights
    def test_admin_name_highlights_matched_words(self):
        response = self.client.get('/api/v1/cities/es-cities/?query=dos')
        self.assertEquals('Antioquia <mark>dos</mark> tres cuatro', response.data[0]['admin_name'])

#Test suggest words mistakes
   # def test_suggests_words_for_spelling_mistakes(self):
   #     response = self.client.get('/api/v1/cities/es-cities-search-words/?query=Bogati')
   #     # Suggestions are: "Bogati" (freq=2) 
   #     #print(response.data)
   #     self.assertEqual(1, len(response.data))
   #     self.assertEqual('bogota', response.data[0]['word'])
        

    #def tearDown(self):
    #    self.mock_constants.stop()
    #    self.connection.indices.delete(index=self.index)