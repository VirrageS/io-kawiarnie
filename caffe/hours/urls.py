from django.conf.urls import url
from django.contrib import admin

from .views import (hours_edit_worked_hours, hours_get_worked_hours,
                    hours_new_worked_hours, hours_get_day_worked_hours)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(
        r'^(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})/$',
        hours_get_day_worked_hours,
        name='show_worked_hours'
    ),
    url(r'^new/$', hours_new_worked_hours, name='new_worked_hours'),
    url(
        r'^edit/(?P<hours_id>\d{0,17})/$',
        hours_edit_worked_hours,
        name='edit_worked_hours'
    ),
    url(
        r'^(?P<hours_id>\d{0,17})/$',
        hours_get_worked_hours,
        name='get_worked_hours'
    )
]
