#!/bin/sh
set -eu

case "${1:-serve}" in
    serve)
        if [ "$#" -gt 0 ]; then
            shift
        fi
        python manage.py migrate --noinput
        exec gunicorn --bind 0.0.0.0:8000 --workers 2 --access-logfile - \
            "$@" daridict.wsgi:application
        ;;
    manage)
        shift
        exec python manage.py "$@"
        ;;
    *)
        exec "$@"
        ;;
esac
