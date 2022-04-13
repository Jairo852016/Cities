# server/start.sh

#!/bin/bash

python ./manage.py migrate
python ./manage.py collectstatic --clear --noinput
python ./manage.py runserver 0.0.0.0:8000
#gunicorn --bind 0.0.0.0:8000 search_cities.wsgi --workers 3