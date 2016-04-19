from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # url(r'^$', reports_show_all_reports, name='reports_show_all'),
]
