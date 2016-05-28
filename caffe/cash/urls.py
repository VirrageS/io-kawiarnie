from django.conf.urls import url
from django.contrib import admin

from .views import (cash_edit_cash_report, cash_edit_company,
                    cash_edit_expense, cash_navigate, cash_new_cash_report,
                    cash_new_company, cash_new_expense,
                    cash_show_all_cash_reports, cash_show_cash_report)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', cash_navigate, name='cash_navigate'),
    url(r'^all/$', cash_show_all_cash_reports, name='show_all_cash_reports'),
    url(r'^show/(?P<report_id>\d{0,17})/$',
        cash_show_cash_report, name='show_cash_report'),

    url(r'^new/company/$', cash_new_company, name='cash_new_company'),
    url(r'^edit/company/(?P<company_id>\d{0,17})/$',
        cash_edit_company, name='cash_edit_company'),

    url(r'^new/expense/$', cash_new_expense, name='cash_new_expense'),
    url(r'^edit/expense/(?P<expense_id>\d{0,17})/$',
        cash_edit_expense, name='cash_edit_expense'),

    url(r'^new/report/$', cash_new_cash_report, name='new_cash_report'),
    url(r'^edit/report/(?P<report_id>\d{0,17})/$',
        cash_edit_cash_report, name='edit_cash_report'),
]
