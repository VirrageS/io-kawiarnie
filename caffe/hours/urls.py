from django.conf.urls import url
from django.contrib import admin

from .views import (hours_edit_position, hours_edit_worked_hours,
                    hours_new_position, hours_new_worked_hours)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^new/$', hours_new_worked_hours, name='new'),
    url(
        r'^edit/(?P<hours_pk>\d{0,17})/$',
        hours_edit_worked_hours,
        name='edit'
    ),

    url(r'^position/new/$', hours_new_position, name='new_position'),
    url(
        r'^position/edit/(?P<position_pk>\d{0,17})/$',
        hours_edit_position,
        name='edit_position'
    ),
]
