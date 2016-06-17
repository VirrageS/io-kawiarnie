from django.conf.urls import url
from django.contrib import admin

from .views import (reports_edit_category, reports_edit_product,
                    reports_edit_report, reports_edit_unit, reports_navigate,
                    reports_new_category, reports_new_product,
                    reports_new_report, reports_new_unit,
                    reports_show_report)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', reports_navigate, name='navigate'),
    url(r'^(?P<report_id>\d{0,17})/$', reports_show_report, name='show'),
    url(r'^new/$', reports_new_report, name='new'),
    url(r'^edit/(?P<report_id>\d{0,17})/$', reports_edit_report, name='edit'),

    url(r'^new/category/$', reports_new_category, name='new_category'),
    url(
        r'^edit/category/(?P<category_id>\d{0,17})/$',
        reports_edit_category,
        name='edit_category'
    ),

    url(r'^new/unit/$', reports_new_unit, name='new_unit'),
    url(
        r'^edit/unit/(?P<unit_id>\d{0,17})/$',
        reports_edit_unit,
        name='edit_unit'
    ),

    url(r'^new/product/$', reports_new_product, name='new_product'),
    url(
        r'^edit/product/(?P<product_id>\d{0,17})/$',
        reports_edit_product,
        name='edit_product'
    ),
]
