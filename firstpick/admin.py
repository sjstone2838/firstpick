from django.contrib import admin

# Register your models here.

from django.contrib import admin
from firstpick.models import *
from .models import *
from django.core import urlresolvers

class UserProfileAdmin(admin.ModelAdmin):
	list_display =('user','id','gender','home_lat','home_lng','events_accepted','events_attended','login_count')
	filter_horizontal = ('sports',)

class SportAdmin(admin.ModelAdmin):
	list_display =('name',)

class EventAdmin(admin.ModelAdmin):
	list_display =('id','organizer','sport','start','location_name','location_lat','location_lng','gender','rating_min','rating_max','players_needed','status')
	list_filter = ('sport', 'organizer')
	filter_horizontal = ('players','invitees')


class SportProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'id', 'sport','radius','rating_count','rating_avg','active')
	list_filter = ('sport','user','active')

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Sport,SportAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(SportProfile,SportProfileAdmin)