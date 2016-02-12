"""
"""
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

from firstpick.models import *
from firstpick.views import *
import datetime
from datetime import timedelta
from itertools import chain


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
app = Celery('mysite')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))

# IN DATABASE, CONFIGURE PERIODIC TASK TO RUN EVERY 15: MIN
@app.task(bind=True)
def send_event_reminders(self):
	# THIS MUST BE RUN EVERY 15:00 MINUTES
	# IF RUN-TIME IS NON-TRIVIAL AND ONLY ONE CELERY WORKER (THREAD),
	# THEN THIS MAY LEAVE GAPS FOR EVENTS WHERE NOTIFICATIONS NOT SENT
	PRECEED_BY = 60 #minutes
	WINDOW = 15 #minutes
	now = datetime.datetime.now()
	start = now + timedelta(minutes = PRECEED_BY)
	end = now + timedelta(minutes = PRECEED_BY + WINDOW)

	events = Event.objects.filter(start__gt = start, start__lte = end)
	for event in events:
		participants = list(chain(User.objects.filter(pk = event.organizer.pk), event.players.all()))
		for participant in participants:
			sender = event.organizer
			recipient = participant
			subject = "Firstpick Reminder: upcoming " + event.sport.name.lower() + " game"
			email_data = {
				'invitee' : recipient,
				'e' : event,
			}
			create_and_send_mail(sender,recipient,subject,email_data,'firstpick/emails/reminder.html','Event Reminder')

