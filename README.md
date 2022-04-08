# Project Cities 

## Installation guide

## Project Organization

        ├── docker-compose.yml
        ├── README.md 
        └── server
            ├── .dockerignore
            ├── Dockerfile
            ├── cities
            │   ├── __init__.py
            │   ├── admin.py
            │   ├── apps.py
            │   ├── filter.py
            │   ├── data
            │   │   └── cities1.json
            │   ├── migrations
            │   │   ├── 0001_initial.py
            │   │   └── __init__.py
            │   ├── models.py
            │   ├── serializers.py
            │   ├── tests
            │   │   ├── __init__.py
            │   │   └── test_views.py
            │   ├── urls.py
            │   └── views.py
            ├── manage.py
            ├── search_cities
            │   ├── __init__.py
            │   ├── asgi.py
            │   ├── settings.py
            │   ├── urls.py
            │   └── wsgi.py
            ├── requirements.txt
            └── start.sh