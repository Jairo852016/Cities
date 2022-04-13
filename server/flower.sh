#!/bin/sh

set -o errexit
set -o nounset


celery flower --app=cities.taskapp --broker='redis://startupy-redis-1:6379/0' --basic_auth="jairo85:123456"