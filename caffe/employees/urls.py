from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from employees.views import (employees_edit_employee, employees_new_employee,
                             employees_logout_employee, employees_navigate,
                             employees_show_all_employees)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', employees_navigate, name='employees_navigate'),

    url(
        r'^login/$', auth_views.login,
        {'template_name': 'employees/login.html'},
        name='login_employee'
    ),
    url(r'^logout/$', employees_logout_employee, name='logout_employee'),
    url(r'^new/$', employees_new_employee, name='new_employee'),
    url(r'^edit/(?P<employee_id>\d{0,17})/$',
        employees_edit_employee, name='edit_employee'),
    url(r'^all/$', employees_show_all_employees, name='show_all_employees'),
]
