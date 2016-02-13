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
from datetime import timedelta, date
from geopy.distance import vincenty
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from itertools import chain


import datetime
import string
import random
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
	#if UserProfile exists
	try:
		user, userProfile = get_user_perms(request)
		upcoming_events = {}

		upcoming_events_player = Event.objects.filter(
			status = "upcoming", 
			players = user,
		)
		upcoming_events_invitee = Event.objects.filter(
			status = "upcoming", 
			invitees = user,
		)
		upcoming_events_organizer = Event.objects.filter(
			status = "upcoming", 
			organizer = user,
		)
		
		upcoming_events = list(chain(upcoming_events_organizer, upcoming_events_invitee, upcoming_events_player))
		upcoming_events.sort(key=lambda r: r.start)
		for e in upcoming_events:
			if e.organizer == user:
				e.relation = "You're the organizer: <a href ='/firstpick/edit_event?eventpk=" + str(e.pk) +"'> Make changes </a>"
			elif e.players.filter(pk = user.pk).count() == 1:
				e.relation = "You're playing: <a href= '/firstpick/rsvp/?userpk=" + str(user.pk) + "&eventpk="+ str(e.pk) +"'> Change </a>"
			else: 
				e.relation = "Invite pending: <a href= '/firstpick/rsvp/?userpk=" + str(user.pk) + "&eventpk="+ str(e.pk) +"'> Respond </a>"
		
		return render_to_response('firstpick/index.html', {
			'user': user,
			'googlekey': settings.GOOGLE_API_KEY,
			'upcoming_events': upcoming_events,
		})
	except:
		return redirect('/firstpick/profile_settings', request = request)
	

def profile_settings(request):
	try:
		user, userProfile = get_user_perms(request)
		#userProfile.gender = SocialAccount.objects.get(user = user).extra_data['gender']
	except:
   		user = request.user
   		userProfile = {}

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

	return render_to_response('firstpick/event.html', {
		'user': user,
		'userProfile': userProfile,	
		'sports': Sport.objects.all(),
		'googlekey': settings.GOOGLE_API_KEY,
	})

def edit_event(request):
	error_msg = None
	user = userProfile = event = {}

	try:
		user, userProfile = get_user_perms(request)
		event = Event.objects.get(pk = request.GET['eventpk'])
		event.date = str('%02d' % event.start.month) + "/" + str('%02d' % event.start.day) + "/" + str(event.start.year)
		event.time = str(event.start.hour) + ":" + str('%02d' % event.start.minute)

		# check that user is event organizer
		if event.organizer != user:
			error_msg = "Sorry - you do not appear to be the organizer of this event"
		else:
			# check that event is upcoming / has not been cancelled or completed
			if event.status == "completed":
				error_msg = "Sorry - this event appears to have already occured"
			else:
				if event.status == "cancelled":
					error_msg = "Sorry - this event appears to have been cancelled"


	except:
		error_msg = "Sorry - we're unable to find that event and/or user"

	return render_to_response('firstpick/event.html', {
		'error_msg': error_msg,
		'event': event,
		'user': user,
		'userProfile': userProfile,	
		'sports': Sport.objects.all(),
		'googlekey': settings.GOOGLE_API_KEY,
	})

def extract_datetime(request):
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
	return datetime.datetime(year,month,day,hour,minute,0)

def create_event(request):
	# CREATE EVENT
	user, userProfile = get_user_perms(request)
	e = Event.objects.create(
		organizer = user,
		name = request.POST['name'],
		sport = Sport.objects.get(name = request.POST['sport']),
		location_name = request.POST['location_name'],
		address = request.POST['address'],
		lat = float(request.POST['lat']),
		lng = float(request.POST['lng']),
		gender = request.POST['gender'],
		rating_min = float(request.POST['rating_min']),
		rating_max = float(request.POST['rating_max']),
		players_needed = int(request.POST['players_needed']),
		status = "upcoming",
		start = extract_datetime(request),
		duration = int(request.POST['duration']),
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
		# Don't invite the organizer
		if e.organizer == ptInvitee:
			continue
		if e.gender == "Male only" and ptInviteeProfile.gender == "Female":
			continue
		if e.gender == "Female only" and ptInviteeProfile.gender == "Male":
			continue
		# CALC VINCENTY DISTANCE IN MILES OF POTENTIAL INVITEE AND EVENT
		# https://pypi.python.org/pypi/geopy
		home_loc = (ptInviteeProfile.home_lat, ptInviteeProfile.home_lng)
		event_loc = (e.lat, e.lng)
		dist = (vincenty(home_loc, event_loc).miles)
		if dist > sp.radius:
			continue
		invitees.append(ptInvitee)
	

	# ADD USERS TO EVENT.INVITEES AND SEND INVITES TO USERS
	for invitee in invitees:
		subject = "Firstpick: new " + e.sport.name.lower() + " game"
		email_data = {
			'invitee' : invitee,
			'e' : e,
		}
		create_and_send_mail(e.organizer,invitee,subject,email_data,'firstpick/emails/invite.html','New Event')
		e.invitees.add(invitee)
		e.save()

	invites_sent = len(invitees)
	return JsonResponse({'invites_sent': invites_sent })

def create_and_send_mail(sender,recipient,subject,email_data,email_template,msg_type):
	body = render_to_string(email_template, email_data)
	send_mail(subject, body, 'invites@deepdive.us ', [recipient.email], fail_silently=False, html_message = body)
	Msg.objects.create(
		sender  = sender, 
		recipient = recipient, 
		subject = subject, 
		body = body, 
		datetime = datetime.datetime.now(),
		msg_type = msg_type,
	)

def save_event(request):
	# TODO: do not allow organizer to reduce players required below players enrolled
	# TODO: do not allow organizer to crop skill range when invites sent to players outside range
	try: 
		user, userProfile = get_user_perms(request)
		e = Event.objects.get(pk = request.POST['eventpk'])
		if e.organizer == user: 
			e.name = request.POST['name']
			e.sport = Sport.objects.get(name = request.POST['sport'])
			e.location_name = request.POST['location_name']
			e.address = request.POST['address']
			e.lat = float(request.POST['lat'])
			e.lng = float(request.POST['lng'])
			e.gender = request.POST['gender']
			e.rating_min = float(request.POST['rating_min'])
			e.rating_max = float(request.POST['rating_max'])
			e.players_needed = int(request.POST['players_needed'])
			e.status = "upcoming"
			e.start = extract_datetime(request)
			e.duration = int(request.POST['duration']),
			e.save()

			for invitee in e.invitees.all():
				subject = "Firstpick: " + e.organizer.first_name + " " + e.organizer.last_name + " changed your upcoming " + e.sport.name.lower() + " game"
				email_data = {
					'invitee' : invitee,
					'e' : e,
				}
				create_and_send_mail(e.organizer,invitee,subject,email_data,'firstpick/emails/event_changed.html','Event Changed')
			status = "success"
		else: 
			status = "failed [USER DOES NOT HAVE ACCESS TO THIS EVENT]"
	except: 
		status = "failed"
	return JsonResponse({'status': status })

def cancel_event(request):
	try:
		user, userProfile = get_user_perms(request)
		e = Event.objects.get(pk = request.POST['eventpk'])
		if e.organizer == user: 
			for invitee in e.invitees.all():
				subject = "Firstpick: " + e.organizer.first_name + " " + e.organizer.last_name + " cancelled your upcoming " + e.sport.name.lower() + " game"
				email_data = {
					'invitee' : invitee,
					'e' : e,
				}
				create_and_send_mail(e.organizer,invitee,subject,email_data,'firstpick/emails/event_cancelled.html','Event Cancelled')
			e.status = "cancelled"
			e.save()
			status = "success"
		else: 
			status = "failed [USER DOES NOT HAVE ACCESS TO THIS EVENT]"
	except: 
		status = "failed"
	return JsonResponse({'status': status })

def check_user_is_invitee(event,user):
	if event.invitees.filter(pk = user.pk).count() == 1:
		return True
	else:
		return False

def check_user_is_player(event,user):
	if event.players.filter(pk = user.pk).count() == 1:
		return True
	else:
		return False

def rsvp(request):
	user = event = error_msg = {}
	try: 
		user = User.objects.get(pk = request.GET['userpk'])
		event = Event.objects.get(pk = request.GET['eventpk'])
	except:
		error_msg = "Something went wrong [UNABLE TO LOCATE USER OR EVENT]"
		return render_to_response('firstpick/rsvp.html', {'error_msg': error_msg})

	if check_user_is_invitee(event,user) or check_user_is_player(event,user):
		user = User.objects.get(pk = request.GET['userpk'])
		event = Event.objects.get(pk = request.GET['eventpk'])
	elif event.organizer == user:
		error_msg = "You appear to be the organizer of this event. If you would like to change the event, please use the 'Change event' button on your home screen"
	else:
		error_msg = "Sorry - it appears you do not have access to this event"

	return render_to_response('firstpick/rsvp.html', {
		'user': user,
		'event': event,
		'error_msg': error_msg,
	})

def check_user_event_perms(event,user):
	try: 
		if check_user_is_player(event,user) == False:
			if check_user_is_invitee(event,user):
				if event.players_needed > 0:
					return True 
				else:
					return "Sorry - this game already filled up"
			else:
				return "Sorry - looks like this game is not open to you"
		else:
			return "You already rsvp'd yes to this event"
			
	except:
		status = "Something went wrong - please try again"

def handle_rsvp(request):
	eventpk = request.POST['vars[eventpk]']
	userpk = request.POST['vars[userpk]']
	rsvp = request.POST['rsvp']
	status = user = event = {}

	try: 
		user = User.objects.get(pk = userpk)
		event = Event.objects.get(pk = eventpk)
	except:
		status = "Something went wrong [UNABLE TO LOCATE USER OR EVENT]"
		return JsonResponse({'status': status })
	
	if rsvp == "yes":
		if check_user_event_perms(event,user):
			event.players.add(user)
			event.invitees.remove(user)
			event.players_needed -= 1
			event.save()
			status = "Great! See you at " + event.location_name + " on " + event.start.strftime('%H:%M%p on %b %d, %Y')
			# SEND CONFIRMATION EMAIL TO ORGANIZER
			subject = "Firstpick: " + user.first_name + " rsvp'd yes to your game"
			email_data = {
				'user' : user,
				'event' : event,
			}
			create_and_send_mail(user,event.organizer,subject,email_data,'firstpick/emails/rsvp_yes.html','RSVP Yes')
		else: 
			status = check_user_event_perms(event, user)
		
	else:
		try: 
			if check_user_is_invitee(event,user):
				event.invitees.remove(user)
				event.save()
				status = "Got it - thanks for your response"
			elif check_user_is_player(event,user):
				event.players.remove(user)
				event.players_needed += 1	
				event.save()		
				status = "Got it - we'll let " + str(event.organizer.first_name) + " know you can't make it"
				# SEND EMAIL TO ORGANIZER
				subject = "Firstpick: " + user.first_name + " can't make it to your game"
				email_data = {
					'user' : user,
					'event' : event,
				}
				create_and_send_mail(user,event.organizer,subject,email_data,'firstpick/emails/rsvp_no.html','RSVP No')	
			else:
				status = "Got it [ERROR]"
		except:
			status = "Got it [ERROR]"
	return JsonResponse({'status': status })

def messages(request):
	user, userProfile = get_user_perms(request)
	messages = Msg.objects.filter(recipient = user).order_by('-datetime')

	return render_to_response('firstpick/messages.html', {
		'user': user,
		'messages': messages,
	})
