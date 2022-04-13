#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


celery -A cities.taskapp beat -l INFO