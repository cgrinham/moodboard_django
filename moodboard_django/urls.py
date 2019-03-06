from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'moodboard_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    path(r'', include('moodboard.urls', namespace='moodboard')),
]
