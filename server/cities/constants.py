#Mapping Elasticsearch

ES_INDEX = 'citie'

ES_MAPPING = {
    'dynamic': 'strict',
    'properties': {
        'citie': {
            'type': 'text',
            "analyzer": "mianalizador",
            'copy_to': 'all_text',
        },
        'lat': {
            'type': 'float',
        },
        'lng': {
            'type': 'float',
        },
        'country': {
            'type': 'keyword',
        },
        'iso2': {
            'type': 'keyword',
        },
        'admin_name': {
            'type': 'text',
            "analyzer": "mianalizador",
            'copy_to': 'all_text',
        },
        'capital': {
            'type': 'keyword',
        },
        'population': {
            'type': 'float',
        },
        'population_proper': {
            'type': 'float',
        },
        'all_text': {
            'type': 'text',
        },
    }
}