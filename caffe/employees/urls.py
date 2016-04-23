from django.conf.urls import url, include
from django.contrib import admin

from employees.views import employees_login_employee, employees_logout_employee

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^login/', employees_login_employee, name='employees_login'),
    url(r'^logout/', employees_logout_employee, name='employees_logout'),
]
