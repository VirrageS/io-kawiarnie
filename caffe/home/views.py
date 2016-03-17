from django.shortcuts import render

from employees.models import Employee


def home_show_employees_view(request):
    employees = Employee.objects.all()

    return render(request, 'home/base.html', {'employees': employees})
