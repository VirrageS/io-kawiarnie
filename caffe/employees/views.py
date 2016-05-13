from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Employee
from .forms import EmployeeForm


def employees_login_employee(request):
    return render(request, 'employees/login.html')


# TODO: create middleware to check if employee is logged in
def employees_logout_employee(request):
    logout(request)
    return render(request, 'employees/logout.html')

def employees_new_employee(request):
    form = []
    form = EmployeeForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(reverse('employees_navigate'))

    return render(request, 'employees/new.html', {
        'form': form
    })


def employees_edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    form = []
    form = EmployeeForm(request.POST or None, instance=employee)

    if form.is_valid():
        form.save()
        return redirect(reverse('employees_navigate'))

    return render(request, 'employees/edit.html', {
        'form': form,
        'employee': employee
    })


def employees_show_all_employees(request):
    employees = Employee.objects.all()

    return render(request, 'employees/all.html', {
        'employees': employees
    })


def employees_navigate(request):
    return render(request, 'home/employees.html')
