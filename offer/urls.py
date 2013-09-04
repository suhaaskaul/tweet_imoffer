from django.conf.urls import patterns, include, url
from offer import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
 
	url(r'^$', 'offer.views.userenter', name='userenter'), 
	url(r'^gettweets/', 'offer.views.gettweets', name='gettweet'),
	url(r'^createoffer/', 'offer.views.createoffer', name='createoffer'),
)
