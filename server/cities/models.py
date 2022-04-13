# server/cities/models.py


import uuid
#Django
from django.contrib.postgres.indexes import GinIndex 
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVectorField, TrigramSimilarity
from django.db import models
from django.db.models import F, Q 


class CitiesQuerySet(models.query.QuerySet): # 
    def search(self, query):
        search_query = Q(
            Q(search_vector=SearchQuery(query))
        )
        return self.annotate(
            citie_headline=SearchHeadline(F('citie'), SearchQuery(query)),
            admin_name_headline=SearchHeadline(F('admin_name'), SearchQuery(query)),
            search_rank=SearchRank(F('search_vector'), SearchQuery(query))
        ).filter(search_query).order_by('-search_rank', 'id')

    
class Cities(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    citie = models.CharField(
        max_length=255, 
        unique=True,
        error_messages={
            'unique':'A city already exists'
        }    
    )
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
    population= models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )
    #models.IntegerField(null=True, blank=True)
    population_proper= models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )
    #models.IntegerField(null=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)
    objects = CitiesQuerySet.as_manager()

    class Meta: # new
        indexes = [
            GinIndex(fields=['search_vector'], name='search_vector_index')
        ]
    

    def __str__(self):
        return f'{self.id}'
    
class SearchHeadline(models.Func):
    function = 'ts_headline'
    output_field = models.TextField()
    template = '%(function)s(%(expressions)s, \'StartSel = <mark>, StopSel = </mark>, HighlightAll=TRUE\')'



class CitiesSearchWordQuerySet(models.query.QuerySet):
    def search(self, query):
        return self.annotate(
            similarity=TrigramSimilarity('word', query)
        ).filter(similarity__gte=0.3).order_by('-similarity')


class CitiesSearchWord(models.Model):
    word = models.CharField(max_length=255, unique=True)

    objects = CitiesSearchWordQuerySet.as_manager()

    def __str__(self):
        return self.word

