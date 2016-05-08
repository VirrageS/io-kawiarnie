from django.conf.urls import url
from django.contrib import admin

from .views import statistics_navigate

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', statistics_navigate, name='statistics_navigate'),
]
