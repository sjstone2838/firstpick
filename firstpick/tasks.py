"""
from celery.task.schedules import crontab
from celery.decorators import periodic_task
#from celery.utils.log import get_task_logger

#from firstpick.utils import save_latest_flickr_image
from firstpick.models import *

logger = get_task_logger(__name__)

@shared_task
@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_create_sport",
    ignore_result=False
)
def task_create_sport():
   	Sport.objects.create(
    	name = "zoomba2"
    )

"""

from celery import task

@task()
def add(x, y):
    return x + y
