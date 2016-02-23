from django.contrib import admin

# Register your models here.

from django.contrib import admin
from firstpick.models import *
from .models import *
from django.core import urlresolvers

class UserProfileAdmin(admin.ModelAdmin):
	list_display =('user','id','gender','address','home_lat','home_lng','events_accepted','events_attended','login_count')
	filter_horizontal = ('sports',)

class SportAdmin(admin.ModelAdmin):
	list_display =('name',)

class EventAdmin(admin.ModelAdmin):
	list_display =('id','organizer','notes','sport','start','location_name','address','lat','lng','gender','rating_min','rating_max','players_needed','status')
	list_filter = ('sport', 'organizer')
	filter_horizontal = ('players','invitees')

class SportProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'id', 'sport','radius','active')
	list_filter = ('sport','user','active')

class MsgAdmin(admin.ModelAdmin):
	list_display = ('sender','recipient','datetime','msg_type','subject')
	list_filter = ('msg_type','sender','recipient')

class RatingAdmin(admin.ModelAdmin):
	list_display = ('player','id','rater','event','sport','datetime','attended','rating')
	list_filter = ('player','rater','event','sport','attended','rating')

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Sport,SportAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(SportProfile,SportProfileAdmin)
admin.site.register(Msg,MsgAdmin)
admin.site.register(Rating,RatingAdmin)