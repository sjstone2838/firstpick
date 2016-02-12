from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib
 
class Sport(models.Model):
	name = models.CharField(max_length=200, unique = True)

	def __unicode__(self):
		return self.name

GENDER_CHOICES = (
	('Male','Male'),
	('Female','Female'),
)

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	gender = models.CharField(max_length=200,
		choices=GENDER_CHOICES,
		default='Male'
	)
	home_lat = models.FloatField(blank = True)
	home_lng = models.FloatField(blank = True)
	events_accepted = models.IntegerField (default = 0)
	events_attended = models.IntegerField (default = 0)
	login_count = models.IntegerField (default = 0)
	sports = models.ManyToManyField(Sport, default = None)

 	# for adding Facebook profile pic to UserProfile
 	# http://www.sarahhagstrom.com/2013/09/the-missing-django-allauth-tutorial/
	def __unicode__(self):
		return "{}'s profile".format(self.user.username)
	class Meta:
		db_table = 'user_profile'
	def account_verified(self):
		if self.user.is_authenticated:
			result = EmailAddress.objects.filter(email=self.user.email)
			if len(result):
				return result[0].verified
		return False
	def profile_image_url(self):
		fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
	 
		if len(fb_uid):
			return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
	 
		return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

ACTIVE_CHOICES = (
	('Yes','Yes'),
	('No','No'),
)

class SportProfile(models.Model):
	user = models.ForeignKey(User)
	sport = models.ForeignKey(Sport)
	radius = models.IntegerField (default = 1)
	# use rating_count to calculate rating_avg
	rating_count =models.IntegerField (default = 0)
	rating_avg = models.FloatField (default = 2.5)
	active = models.CharField(max_length=100, choices=ACTIVE_CHOICES, default = "Yes")

GENDER_PREFERENCES = (
	('No gender preference','No gender preference'),
	('Male only','Male only'),
	('Female only','Female only'),
)

EVENT_STATUS = (
	('completed', 'completed'),
	('cancelled','cancelled'),
	('occurring','occurring'),
	('upcoming','upcoming'),
)

class Event(models.Model):
	organizer = models.ForeignKey(User)
	name = models.CharField(max_length = 500)
	sport = models.ForeignKey(Sport)
	start = models.DateTimeField('Start time')
	duration = models.IntegerField(default = 60)
	location_name = models.CharField(max_length = 500)
	address = models.CharField(max_length = 500)
	lat = models.FloatField (default = 0)
	lng = models.FloatField (default = 0)
	gender = models.CharField(max_length=200, choices=GENDER_PREFERENCES)
	rating_min = models.DecimalField(max_digits=5, decimal_places=2)
	rating_max = models.DecimalField(max_digits=5, decimal_places=2)
	players_needed = models.IntegerField (default = 0)
	status = models.CharField(max_length=200, choices=EVENT_STATUS)
	invitees = models.ManyToManyField(User, default = None, related_name = "Invitees")
	players = models.ManyToManyField(User, default = None, related_name = "Players")
	
	def __unicode__(self):
		return str(self.name)

MSG_CHOICES = (
	('New Event', 'New Event'),
	('RSVP Yes','RSVP Yes'),
	('RSVP No','RSVP No'),
	('Event Changed','Event Changed'),
	('Event Cancelled','Event Cancelled'),
	('Event Reminder','Event Reminder'),
)

class Msg(models.Model):
	sender = models.ForeignKey(User, related_name = "Sender")
	recipient = models.ForeignKey(User, related_name = "Recipient")
	datetime = models.DateTimeField('Sent at')
	subject = models.TextField(default="No Subject")
	body = models.TextField(default="No Body")
	msg_type = models.CharField(max_length=200, choices=MSG_CHOICES)
	
	def __unicode__(self):
		return str(self.sender) + " to" + str(self.recipient) + " re: " + str(self.subject)


