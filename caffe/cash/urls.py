from django.conf.urls import url
from django.contrib import admin

from .views import (cash_edit_cash_report, cash_edit_company,
                    cash_edit_expense, cash_navigate, cash_new_cash_report,
                    cash_new_company, cash_new_expense,
                    cash_show_cash_report)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', cash_navigate, name='navigate'),
    url(r'^(?P<report_id>\d{0,17})/$', cash_show_cash_report, name='show'),
    url(r'^new/$', cash_new_cash_report, name='new'),
    url(
        r'^edit/(?P<report_id>\d{0,17})/$',
        cash_edit_cash_report,
        name='edit'
    ),

    url(r'^new/company/$', cash_new_company, name='new_company'),
    url(
        r'^edit/company/(?P<company_id>\d{0,17})/$',
        cash_edit_company,
        name='edit_company'
    ),

    url(r'^new/expense/$', cash_new_expense, name='new_expense'),
    url(r'^edit/expense/(?P<expense_id>\d{0,17})/$',
        cash_edit_expense, name='edit_expense'),
]
