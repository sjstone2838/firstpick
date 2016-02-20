web: python manage.py collectstatic --noinput; gunicorn mysite.wsgi
worker: python manage.py celery worker --without-gossip --without-mingle --without-heartbeat -B -l info 

