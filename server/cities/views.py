# server/cities/views.py

from elasticsearch_dsl import Search 
from elasticsearch_dsl.query import Match, Term 
from rest_framework.generics import ListAPIView
from rest_framework.response import Response 
from rest_framework.views import APIView 

import csv
from import_export import resources

from . import constants

from .models import Cities, CitiesSearchWord 
from .serializers import CitiesSerializer, CitiesSearchWordSerializer
from .filter import CitiesFilterSet, CitiesSearchWordFilterSet


class CitiesView(ListAPIView):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer
    filterset_class = CitiesFilterSet

    def filter_queryset(self, request):
        return super().filter_queryset(request)[:100]

class CitiesSearchWordsView(ListAPIView):
    queryset = CitiesSearchWord.objects.all()
    serializer_class = CitiesSearchWordSerializer
    filterset_class = CitiesSearchWordFilterSet


#class CitiesView(ListAPIView):
#    serializer_class = CitiesSerializer

#    def get_queryset(self):
#        queryset = Cities.objects.all()
#        country = self.request.query_params.get('country')
#        if country is not None:
            # Additional type checking...
#            queryset = queryset.filter(country=country)
#        capital = self.request.query_params.get('capital')
#        if capital:
#            # Additional type checking...
#            queryset = queryset.filter(capital=capital)
#        query = self.request.query_params.get('query')
#        if query:
#            queryset = queryset.filter(Q(
#                Q(citie__contains=query) |
#                Q(admin_name__contains=query)
#            ))
#        return queryset

class ESCitiesView(APIView):
    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('query')
        country = self.request.query_params.get('country')
        
        # Build Elasticsearch query.
        search = Search(index=constants.ES_INDEX)
        q = {'should': [], 'filter': []}
        # Build should clause.
        if query:
            q['should'] = [
                Match(citie={'query': query, 'boost': 3.0}),
                Match(admin_name={'query': query, 'boost': 2.0})
            
            ]
            q['minimum_should_match'] = 1

            # Build highlighting.
            search = search.highlight_options( 
                number_of_fragments=0,
                pre_tags=['<mark>'],
                post_tags=['</mark>']
            )
            search = search.highlight('citie', 'admin_name') 

        # Build filter clause.
        if country:
            q['filter'].append(Term(country=country))

        response = search.query('bool', **q).params(size=100).execute()
       
        if response.hits.total.value > 0:
            return Response(data=[{
                'id': hit.meta.id,
                'citie': (
                    hit.meta.highlight.citie[0]
                    if 'highlight' in hit.meta and 'citie' in hit.meta.highlight
                    else hit.citie
                ),
                'lat': hit.lat,
                'lng': hit.lng,
                'country': hit.country,
                'iso2': hit.iso2,
                'admin_name': (
                    hit.meta.highlight.admin_name[0]
                    if 'highlight' in hit.meta and 'admin_name' in hit.meta.highlight
                    else hit.admin_name
                ),
                'capital': hit.capital,
                'population': hit.population,
                'population_proper': hit.population_proper,
             
            } for hit in response])
        else:
            return Response(data=[])

class ESCitiesSearchWordsView(APIView):
    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('query')

        # Build Elasticsearch query.
        search = Search().suggest('result', query, term={
            'field': 'all_text'
        })

        response = search.execute()

        # Extract words.
        options = response.suggest.result[0]['options']
        words = [{'word': option['text']} for option in options]

        return Response(data=words)


class ImportView(ListAPIView):
    def get(self, request, *args, **kwargs):
   # def import_csv(request):
        print("hola")
        citiesS = []
        with open("cities.csv", "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            print(data[1][0],data[1][1],data[1][2],data[1][3],data[1][4],data[1][5],data[1][6],data[1][7],data[1][8])
            for row in data[1:]:
                citiesS.append(
                    Cities(
                        citie=row[0],
                        lat=row[1],
                        lng=row[2],
                        country=row[3],
                        iso2=row[4],
                        admin_name=row[5],
                        capital=row[6],
                        population=int(float(row[7])),
                        population_proper=int(float(row[8]))
                        
                    )
                
                )
        #print("Prueba: ",citiesS[0].)  
        if len(citiesS) > 0:
            Cities.objects.bulk_create(citiesS)
        
        return Response("Successfully imported")

