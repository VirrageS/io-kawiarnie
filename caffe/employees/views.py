from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout


from .models import Employee
from .forms import EmployeeForm


@login_required
def employees_logout_employee(request):
    logout(request)

    return render(request, 'employees/logout.html')


def employees_new_employee(request):
    new_emp_form = EmployeeForm(request.POST or None)

    if new_emp_form.is_valid():
        new_emp_form.save()
        return redirect(reverse('employees_navigate'))

    return render(request, 'employees/new.html', {
        'form': new_emp_form
    })


def employees_edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    edit_emp_form = EmployeeForm(request.POST or None, instance=employee)

    if edit_emp_form.is_valid():
        edit_emp_form.save()
        return redirect(reverse('employees_navigate'))

    return render(request, 'employees/edit.html', {
        'form': edit_emp_form,
        'employee': employee
    })


def employees_show_all_employees(request):
    employees = Employee.objects.all()

    return render(request, 'employees/all.html', {
        'employees': employees
    })


def employees_navigate(request):
    return render(request, 'home/employees.html')
