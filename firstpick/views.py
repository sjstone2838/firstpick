from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.template import loader
from django.db.models import Avg
from django.template.context import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth import authenticate,login, logout

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime
from datetime import timedelta, date
from django.utils import timezone
from geopy.distance import vincenty
import json
import re
from firstpick.models import *

user = {}

def get_user_perms(request):
	user = request.user
	userProfile = UserProfile.objects.get(user = user)
	return (user, userProfile)

@login_required(login_url = '/accounts/login/')
def index(request):
	#if UserProfile exists:
	try:
		user, userProfile = get_user_perms(request)
	except:
		return redirect('/firstpick/profile_settings', request = request)
	
	return render_to_response('firstpick/index.html', {
		'user': user,
		'googlekey': settings.GOOGLE_API_KEY,	
	})

def profile_settings(request):
	try:
		user, userProfile = get_user_perms(request)
		userProfile.gender = SocialAccount.objects.get(user = user).extra_data['gender']
	except:
   		user = request.user
   		userProfile = {}
   		userProfile['gender'] = "Gender"

	return render_to_response('firstpick/profile_settings.html', {
		'user': user,
		'userProfile': userProfile,
		'googlekey': settings.GOOGLE_API_KEY,
		'sports': Sport.objects.all(),	
	})

def save_profile(request):
	user = request.user
	userProfile = {}
	status = ""
	user.first_name = request.POST['first_name']
	user.last_name = request.POST['last_name']
	user.email = request.POST['email']
	user.save()

	try:
		userProfile = UserProfile.objects.get(user = user)
		userProfile.gender = request.POST['gender']
		userProfile.home_lat = request.POST['home_lat']
		userProfile.home_lng = request.POST['home_lng']
		userProfile.save()
		status = "Existing profile saved"
		# delete all sports associted with UP, then add them back later
		userProfile.sports.through.objects.all().delete()
	
	except:
		userProfile = UserProfile.objects.create(
			user = user,
			gender = request.POST['gender'],
			home_lat = request.POST['home_lat'],
			home_lng = request.POST['home_lng'],
		)
		status = "Created new profile"
	
	# set all SportProfile objects for User to inactive, then reset those that have been selected
	for sp in SportProfile.objects.filter(user = user):
		sp.active = "No"
		sp.save()

	for i in range (0, int(request.POST['sport_count'])):
		sport = Sport.objects.get(name = request.POST["sport_profiles[" + str(i) + "][sport]"])
		userProfile.sports.add(sport)
		radius = int(request.POST["sport_profiles[" + str(i) + "][radius]"])
		stars = float(request.POST["sport_profiles[" + str(i) + "][stars]"])

		try: 
			sp = SportProfile.objects.get(user = user, sport = sport)
			# adjust rating_avg by adding one new rating
			new_avg = (sp.rating_avg * sp.rating_count + stars) / (sp.rating_count + 1)
			sp.radius = radius
			sp.active = "Yes"
			sp.rating_avg = new_avg
			sp.rating_count += 1
			sp.save()
		except:
			SportProfile.objects.create(
				user = user, 
				sport = sport,
				radius = radius,
				rating_avg = stars,
				rating_count = 1,
			)

	return JsonResponse({'status': status})	

def new_event(request):
	user, userProfile = get_user_perms(request)

	return render_to_response('firstpick/new_event.html', {
		'user': user,
		'userProfile': userProfile,	
		'sports': Sport.objects.all(),
		'googlekey': settings.GOOGLE_API_KEY,
	})

def create_event(request):
	# CREATE EVENT
	user, userProfile = get_user_perms(request)
	month = int(request.POST['date'].split("/")[0])
	day = int(request.POST['date'].split("/")[1])
	year = int(request.POST['date'].split("/")[2])
	hour = int(request.POST['time'].split(":")[0])
	minute = int(request.POST['time'].split(":")[1][:2])
	am_pm = request.POST['time'].split(":")[1][-2:]
	if hour != 12  and am_pm == "pm":
		hour += 12
	if hour == 12 and am_pm == "am":
		hour = 0

	e = Event.objects.create(
		organizer = user,
		name = request.POST['name'],
		sport = Sport.objects.get(name = request.POST['sport']),
		location_name = request.POST['location_name'],
		location_lat = float(request.POST['lat']),
		location_lng = float(request.POST['lng']),
		gender = request.POST['gender'],
		rating_min = float(request.POST['rating_min']),
		rating_max = float(request.POST['rating_max']),
		players_needed = int(request.POST['players_needed']),
		status = "upcoming",
		start = datetime.datetime(year,month,day,hour,minute,0)
	)

	# FIND ALL USERS WHO MEET CRITERIA
	# first filter Sport Profiles
	sps = SportProfile.objects.filter(
		active = "Yes",
		sport = e.sport,
		rating_avg__gte = e.rating_min,
		rating_avg__lte = e.rating_max,
	)

	# then filter user / userprofiles based on gender and proximity
	invitees = []
	for sp in sps:
		ptInvitee = sp.user
		ptInviteeProfile = UserProfile.objects.get(user = ptInvitee)
		
		if e.gender == "Male only" and ptInviteeProfile.gender == "Female":
			continue
		if e.gender == "Female only" and ptInviteeProfile.gender == "Male":
			continue
		# CALC VINCENTY DISTANCE IN MILES OF POTENTIAL INVITEE AND EVENT
		# https://pypi.python.org/pypi/geopy
		home_loc = (ptInviteeProfile.home_lat, ptInviteeProfile.home_lng)
		event_loc = (e.location_lat, e.location_lng)
		dist = (vincenty(home_loc, event_loc).miles)
		if dist > sp.radius:
			continue
		invitees.append(ptInvitee)
	

	# ADD USERS TO EVENT.INVITEES AND SEND INVITES TO USERS
	for invitee in invitees:
		print "Hi " + invitee.first_name + ", You're invited to play " + e.sport.name + " on " + str(e.start)
		



		e.invitees.add(invitee)
		e.save()

	invites_sent = len(invitees)
	return JsonResponse({'invites_sent': invites_sent })


