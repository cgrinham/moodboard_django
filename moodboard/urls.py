from django.conf.urls import patterns, url

from moodboard import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<username>\w+)$', views.user, name='user'),
    url(r'^user/(?P<username>\w+)/dir/(?P<directory>\w+)$', views.user, name='userdir'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
)

# url(r'^userdb/(?P<username>\w+)$', views.userdb, name='userdb'),
# url(r'^userdb/(?P<username>\w+)/(?P<tag>\w+)$', views.userdb, name='usertag'),
# url(r'^user/(?P<username>\w+)/account$', views.useraccount, name='useraccount'),
