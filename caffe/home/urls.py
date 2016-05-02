from django.conf.urls import url
from django.contrib import admin

from home.views import home_show_employees_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', home_show_employees_view, name='home_show_employees'),
]
