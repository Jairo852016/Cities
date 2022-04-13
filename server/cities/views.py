# server/cities/views.py

#Elasticsearch
from elasticsearch_dsl import Search 
from elasticsearch_dsl.query import Match, Term 

#Django REST Framework
from rest_framework.generics import ListAPIView
from rest_framework.response import Response 
from rest_framework.views import APIView 
#from django.views.generic.edit import CreateView

#Django
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.conf import settings 

#Model Serializer Filter
from .models import Cities, CitiesSearchWord
from .serializers import CitiesSerializer, CitiesSearchWordSerializer
from .filter import CitiesFilterSet, CitiesSearchWordFilterSet
from .pagination import CustumPageNumberPagination

#Constants
from . import constants

#Externos
import csv
import pathlib 

#taks
from cities.taskapp.task import sleep_for



class CitiesView(ListAPIView):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer
    #pagination_class = CustumPageNumberPagination
    filterset_class = CitiesFilterSet

    def filter_queryset(self, request):
        return super().filter_queryset(request)[:100]

class CitiesPaginationView(ListAPIView):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer
    pagination_class = CustumPageNumberPagination
    filterset_class = CitiesFilterSet

class CitiesSearchWordsView(ListAPIView):
    queryset = CitiesSearchWord.objects.all()
    serializer_class = CitiesSearchWordSerializer
    filterset_class = CitiesSearchWordFilterSet


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

#Function Upload CSV method POST
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        #print( context['url'])
        data_path = pathlib.Path(settings.BASE_DIR / 'media' / uploaded_file.name )
        
        with open(data_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                queryset = Cities.objects.all()
                d = queryset.filter( citie=row[0])
                if row[7]=="":
                    a=0
                else:
                    a=row[7]
                if row[8]=="":
                    e=0
                else:
                    e=row[8]
                if  len(d)>0:
                   
                    d[0].lat=row[1]
                    d[0].lng=row[2]
                    d[0].country=row[3]
                    d[0].iso2=row[4]
                    d[0].admin_name=row[5]
                    d[0].capital=row[6]
                    d[0].population=a                   
                    d[0].population_proper=e
                    d[0].save()
                else:
                    c = Cities(
                        citie=row[0],
                        lat=row[1],
                        lng=row[2],
                        country=row[3],
                        iso2=row[4],
                        admin_name=row[5],
                        capital=row[6],
                        population=a,                    
                        population_proper=e
                    )
                    c.save()
        sleep_for.delay()
        #handle_Elastic()
    return render(request, 'cities/upload.html', context)


