"""caffe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from .views import reports_show_all_reports, reports_create, reports_show_report
from .views import reports_new_category, reports_new_unit, reports_new_product
from .views import reports_new_fullproduct, reports_new_report

from .views import reports_edit_category, reports_edit_unit, reports_edit_report
from .views import reports_edit_product, reports_edit_fullproduct

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', reports_show_all_reports, name='reports_show_all'),
    url(r'^new/$', reports_create, name='reports_create'),

    url(r'^new/category/$', reports_new_category, name='reports_new_category'),
    url(r'^edit/category/(?P<category_id>\d+)/$',
        reports_edit_category, name='reports_edit_category'),

    url(r'^new/unit/$', reports_new_unit, name='reports_new_unit'),
    url(r'^edit/unit/(?P<unit_id>\d+)/$',
        reports_edit_unit, name='reports_edit_unit'),

    url(r'^new/product/$', reports_new_product, name='reports_new_product'),
    url(r'^edit/product/(?P<product_id>\d+)/$',
        reports_edit_product, name='reports_edit_product'),

    url(r'^new/fullproduct/$',
        reports_new_fullproduct, name='reports_new_fullproduct'),
    url(r'^edit/fullproduct/(?P<fullproduct_id>\d+)/$',
        reports_edit_fullproduct, name='reports_edit_fullproduct'),

    url(r'^new/report/$', reports_new_report, name='reports_new_report'),
    url(r'^edit/report/(?P<report_id>\d+)/$',
        reports_edit_report, name='reports_edit_report'),

    url(r'^show/(?P<report_id>\d+)/$',
        reports_show_report, name='reports_show_report'),
]
