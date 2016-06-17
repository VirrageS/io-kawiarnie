from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from employees.views import (employees_delete_employee,
                             employees_edit_employee,
                             employees_logout_employee, employees_navigate,
                             employees_new_employee,
                             employees_show_all_employees)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', employees_navigate, name='navigate'),

    url(r'^all/$', employees_show_all_employees, name='all'),
    url(r'^new/$', employees_new_employee, name='new'),
    url(
        r'^edit/(?P<employee_id>\d{0,17})/$',
        employees_edit_employee,
        name='edit'
    ),
    url(
        r'^delete/(?P<employee_id>\d{0,17})/$',
        employees_delete_employee,
        name='delete'
    ),

    url(
        r'^login/$', auth_views.login,
        {'template_name': 'employees/login.html'},
        name='login'
    ),
    url(r'^logout/$', employees_logout_employee, name='logout'),
]
