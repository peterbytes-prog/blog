#!/bin/sh
set -e
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata users.json

# uwsgi --socket :8000 --master --enable-threads --module guestlist.wsgi:application

uwsgi --module=blog.wsgi:application \
--env=DJANGO_SETTINGS_MODULE=blog.settings_pro \
--master --socket :8000 \
--enable-threads
