from django.conf.urls import include, url
from django.contrib import admin

from .views import index_navigate

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', index_navigate, name='index_navigate'),
    url(r'cafe/', include('home.urls')),
    url(r'reports/', include('reports.urls')),
    url(r'stencils/', include('stencils.urls')),
    url(r'employees/', include('employees.urls')),
    url(r'statistics/', include('stats.urls')),
    url(r'calendar/', include('calendars.urls')),
    url(r'hours/', include('hours.urls')),
    url(r'cash/', include('cash.urls')),
]
