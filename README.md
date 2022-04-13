
# Project Cities 
> Short blurb about what your product does.
[![LinkedIn][linkedin-shield]][linkedin-url]

## Installation guide

## Project Organization
    
    
    └──
        ├── docker-compose.yml
        ├── README.md 
        └──client
        │   ├── package-lock.json
        │   ├── package.json
        │   ├── Dockerfile
        │   ├── .dockerignore
        │   └── src
        │       ├── components   
        │       │   ├── Bootstrapb1.js
        │       │   ├── ResulList.js
        │       │   └── Search.js
        │       ├── App.js
        │       ├── App.test.js
        │       ├── index.css
        │       ├── index.js
        │       └── log.svg
        └──reverse-proxy
        │   ├── Dockerfile
        │   └── nginx.conf
        └── server
            ├── .dockerignore
            ├── Dockerfile
            ├── cities
            │   ├── data
            │   ├── fixtures        
            │   │   └── test_citie.json
            │   ├── management   
            │   │   └── commands
            │   │       ├── __init__.py
            │   │       ├── bulk_update.py
            │   │       ├── create_index.py
            │   │       └── elasticsearch.py
            │   ├── __init__.py
            │   ├── admin.py
            │   ├── constants.py
            │   ├── pagination.py
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
            │   ├── task
            │   │   ├── __init__.py
            │   │   ├── celery.py
            │   │   └── task.py
            │   ├── templates
            │   │   └── cities
            │   │       └── upload.html
            │   ├── urls.py
            │   └── views.py
            ├── manage.py
            ├── media
            ├── static
            ├── search_cities
            │   ├── __init__.py
            │   ├── asgi.py
            │   ├── settings.py
            │   ├── urls.py
            │   └── wsgi.py
            ├── requirements.txt
            ├── beat.sh
            ├── flower.sh
            ├── worker.sh
            └── start.sh


[linkedin-url]: https://linkedin.com/in/othneildrew