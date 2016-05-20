from django.conf.urls import url
from django.contrib import admin

from calendars.views import calendar_navigate, calendar_show_day

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', calendar_navigate, name='calendar_navigate'),

    url(
        r'^(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})/$',
        calendar_show_day,
        name='show_day'
    ),
]
