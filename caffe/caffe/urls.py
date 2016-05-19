from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'', include('home.urls')),
    url(r'reports/', include('reports.urls')),
    url(r'stencils/', include('stencils.urls')),
    url(r'employees/', include('employees.urls')),
    url(r'statistics/', include('stats.urls')),
    url(r'calendar/', include('calendars.urls')),
]
