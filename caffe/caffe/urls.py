from django.conf.urls import include, url
from django.contrib import admin

from .views import index_navigate, caffe_create

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', index_navigate, name='index_navigate'),
    url(r'^create/$', caffe_create, name='caffe_create'),

    url(r'cafe/', include('home.urls', namespace='home')),
    url(r'reports/', include('reports.urls', namespace='reports')),
    url(r'stencils/', include('stencils.urls', namespace='stencils')),
    url(r'employees/', include('employees.urls', namespace='employees')),
    url(r'statistics/', include('stats.urls', namespace='statistics')),
    url(r'calendar/', include('calendars.urls', namespace='calendar')),
    url(r'hours/', include('hours.urls', namespace='hours')),
    url(r'cash/', include('cash.urls', namespace='cash')),
]
