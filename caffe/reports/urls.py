from django.conf.urls import url
from django.contrib import admin

from .views import \
    reports_show_all_reports, reports_create, reports_new_category,\
    reports_new_unit, reports_new_product, reports_new_fullproduct,\
    reports_new_report, reports_show_report, reports_edit_category,\
    reports_edit_unit, reports_edit_product, reports_edit_fullproduct,\
    reports_edit_report

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', reports_show_all_reports, name='reports_show_all'),
    url(r'^new/$', reports_create, name='reports_create'),
    url(r'^show/(?P<report_id>\d{0,17})/$',
        reports_show_report, name='reports_show_report'),

    url(r'^new/category/$', reports_new_category, name='reports_new_category'),
    url(r'^edit/category/(?P<category_id>\d{0,17})/$',
        reports_edit_category, name='reports_edit_category'),

    url(r'^new/unit/$', reports_new_unit, name='reports_new_unit'),
    url(r'^edit/unit/(?P<unit_id>\d{0,17})/$',
        reports_edit_unit, name='reports_edit_unit'),

    url(r'^new/product/$', reports_new_product, name='reports_new_product'),
    url(r'^edit/product/(?P<product_id>\d{0,17})/$',
        reports_edit_product, name='reports_edit_product'),

    url(r'^new/fullproduct/$',
        reports_new_fullproduct, name='reports_new_fullproduct'),
    url(r'^edit/fullproduct/(?P<fullproduct_id>\d{0,17})/$',
        reports_edit_fullproduct, name='reports_edit_fullproduct'),

    url(r'^new/report/$', reports_new_report, name='reports_new_report'),
    url(r'^edit/report/(?P<report_id>\d{0,17})/$',
        reports_edit_report, name='reports_edit_report'),
]
