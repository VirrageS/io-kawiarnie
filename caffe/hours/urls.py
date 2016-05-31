from django.conf.urls import url
from django.contrib import admin

from .views import (hours_edit_worked_hours,
                    hours_new_worked_hours)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^new/$', hours_new_worked_hours, name='new_worked_hours'),
    url(
        r'^edit/(?P<hours_id>\d{0,17})/$',
        hours_edit_worked_hours,
        name='edit_worked_hours'
    ),
]
