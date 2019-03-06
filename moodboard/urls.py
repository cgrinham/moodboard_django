from django.urls import path
from django.contrib.auth.views import LoginView

from moodboard import views

app_name = "moodboard"

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'^user/(?P<username>\w+)$', views.user, name='user'),
    path(r'^user/(?P<username>\w+)/dir/(?P<directory>\w+)$', views.user, name='userdir'),
    path(r'^login$', LoginView.as_view(template_name='users/login.html'), name='login'),
    path(r'^logout$', views.logout, name='logout'),
    path(r'^register$', views.register, name='register'),
]

# url(r'^userdb/(?P<username>\w+)$', views.userdb, name='userdb'),
# url(r'^userdb/(?P<username>\w+)/(?P<tag>\w+)$', views.userdb, name='usertag'),
# url(r'^user/(?P<username>\w+)/account$', views.useraccount, name='useraccount'),
