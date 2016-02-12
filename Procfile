web: python manage.py collectstatic --noinput; gunicorn mysite.wsgi
worker: python manage.py celery worker -B -l info

