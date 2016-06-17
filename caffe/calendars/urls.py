from django.conf.urls import url
from django.contrib import admin

from calendars.views import calendar_navigate, calendar_show_day

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', calendar_navigate, name='navigate'),

    url(
        r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$',
        calendar_show_day,
        name='show_day'
    ),
]
