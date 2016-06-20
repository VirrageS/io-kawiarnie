from django.conf.urls import url
from django.contrib import admin

from home.views import caffe_navigate

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', caffe_navigate, name='navigate'),
]
