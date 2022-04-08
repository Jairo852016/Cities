# server/cities/tests/test_views.py

from rest_framework.test import APIClient, APITestCase

from cities.models import Cities


class ViewTests(APITestCase):

    def test_empty_query_returns_everything(self):
        citie = Cities.objects.create(
            
            citie = 'Bogotá',
            lat =4.6126,
            lng = -74.0705,
            country = 'Colombia',
            iso2 = 'CO',
            admin_name = 'Bogotá', 
            capital= 'primary',
            population= 9464000,
            population_proper= 7963000
        )
        client = APIClient()
        response = client.get('/api/v1/cities/cities/')
        self.assertJSONEqual(response.content, [{
            'id': str(citie.id),
            'citie' : 'Bogotá',
            'lat' : '4.6126',
            'lng' : '-74.0705',
            'country' : 'Colombia',
            'iso2' : 'CO',
            'admin_name' : 'Bogotá', 
            'capital' : 'primary',
            'population': 9464000,
            'population_proper': 7963000,
            
        }])