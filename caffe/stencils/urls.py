from django.conf.urls import url
from django.contrib import admin

from .views import (stencils_edit_stencil, stencils_new_report,
                    stencils_new_stencil, stencils_show_all_stencils,
                    stencils_show_stencil)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^all/$', stencils_show_all_stencils, name='all'),
    url(
        r'^show/(?P<stencil_id>\d{0,17})/$',
        stencils_show_stencil,
        name='show'
    ),
    url(r'^new/$', stencils_new_stencil, name='new'),
    url(
        r'^edit/(?P<stencil_id>\d{0,17})/$',
        stencils_edit_stencil,
        name='edit'
    ),

    url(r'^new/report/(?P<stencil_id>\d{0,17})/$',
        stencils_new_report, name='new_report'),
]
