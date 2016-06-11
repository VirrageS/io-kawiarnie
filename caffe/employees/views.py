"""Module with views for the employee feature."""

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm
from .models import Employee


@login_required
def employees_logout_employee(request):
    """Logout a user, default behaviour."""

    logout(request)

    return render(request, 'employees/logout.html')


@permission_required('employees.add_employee')
def employees_new_employee(request):
    """Create a new employee."""

    form = EmployeeForm(request.POST or None, caffe=request.user.caffe)

    if form.is_valid():
        form.save()
        messages.success(request, 'Pracownik został poprawnie stworzony.')
        return redirect(reverse('employees_navigate'))
    elif request.POST:
        messages.error(request, u'Formularz został niepoprawnie wypełniony.')

    return render(request, 'employees/new.html', {
        'form': form
    })


@permission_required('employees.change_employee')
def employees_edit_employee(request, employee_id):
    """Edit an employee."""

    employee = get_object_or_404(
        Employee,
        id=employee_id,
        caffe=request.user.caffe
    )

    form = EmployeeForm(
        request.POST or None,
        instance=employee,
        caffe=request.user.caffe
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Pracownik został poprawnie zmieniony.')
        return redirect(reverse('employees_navigate'))
    elif request.POST:
        messages.error(request, u'Formularz został niepoprawnie wypełniony.')

    return render(request, 'employees/edit.html', {
        'form': form,
        'employee': employee
    })


@permission_required('employees.delete_employee')
def employees_delete_employee(request, employee_id):
    """Delete an employee."""

    employee = get_object_or_404(
        Employee,
        id=employee_id,
        caffe=request.user.caffe
    )

    if employee == request.user:
        messages.error(request, u'Nie możesz usunąć siebie.')
        return redirect(reverse('employees_navigate'))

    employee.delete()
    messages.success(request, u'Pracownik został poprawnie usunięty.')
    return redirect(reverse('employees_navigate'))


@permission_required('employees.view_employee')
def employees_show_all_employees(request):
    """Show all employees."""

    employees = (Employee
        .objects
        .order_by('last_name', 'first_name')
        .filter(caffe=request.user.caffe)
        .all()
    )

    return render(request, 'employees/all.html', {
        'employees': employees
    })


@permission_required('employees.view_employee')
def employees_navigate(request):
    """Show main employee page."""

    return render(request, 'home/employees.html')
