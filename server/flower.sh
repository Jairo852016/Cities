#!/bin/sh

set -o errexit
set -o nounset

celery  --app=cities.taskapp  --broker='redis://startupy-redis-1:6379/0' flower --basic_auth="jairo85:123456"
#celery flower --app=cities.taskapp --broker='redis://startupy-redis-1:6379/0' --basic_auth="jairo85:123456"
#celery flower \
#    --app=cities.taskapp \
#    --broker="${CELERY_BROKER_URL}" \
#    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"