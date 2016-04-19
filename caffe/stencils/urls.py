from django.conf.urls import url
from django.contrib import admin

from .views import \
    stencils_create, stencils_new_stencil, stencils_new_report, \
    stencils_show

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^create/$', stencils_create, name='stencils_create'),
    url(r'^new/stencil/$', stencils_new_stencil, name='stencils_new_stencil'),
    url(r'^new/report/$', stencils_new_report, name='stencils_new_report'),
    url(r'^show/$', stencils_show, name='stencils_show'),
]
