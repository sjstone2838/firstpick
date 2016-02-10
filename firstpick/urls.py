from django.conf.urls import *
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.static import serve

urlpatterns = patterns('firstpick.views',
	(r'^$', 'index'),
	(r'^profile_settings/$','profile_settings'),
	(r'^save_profile/$','save_profile'),
	(r'^new_event/$','new_event'),
	(r'^edit_event/$','edit_event'),
	(r'^create_event/$','create_event'),
	(r'^save_event/$','save_event'),
	(r'^rsvp/$','rsvp'),
	(r'^handle_rsvp/$','handle_rsvp'),
	(r'^messages/$','messages'),
)