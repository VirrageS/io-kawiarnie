from django.conf.urls import url
from django.contrib import admin

from .views import (stencils_create, stencils_edit_report,
                    stencils_edit_stencil, stencils_new_report,
                    stencils_new_stencil, stencils_show_all_stencils,
                    stencils_show_stencil)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^create/$', stencils_create, name='stencils_create'),
    url(r'^show/(?P<stencil_id>\d{0,17})/$',
        stencils_show_stencil, name='stencils_show_stencil'),

    url(r'^new/stencil/$', stencils_new_stencil, name='stencils_new_stencil'),
    url(r'^edit/stencil/(?P<stencil_id>\d{0,17})/$',
        stencils_edit_stencil, name='stencils_edit_stencil'),

    url(r'^show/all/$',
        stencils_show_all_stencils, name='stencils_show_all_stencils'),
    url(r'^new/report/(?P<stencil_id>\d{0,17})/$', stencils_new_report, name='stencils_new_report'),
    url(r'^edit/report/(?P<report_id>\d{0,17})/$',
        stencils_edit_report, name='stencils_edit_report'),
]
