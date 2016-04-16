from django.shortcuts import render, render_to_response
from django.template import RequestContext

from employees.models import Employee


def home_show_employees_view(request):
    employees = Employee.objects.all()

    return render(request, 'home/base.html', {'employees': employees})


def handler404(request):
    response = render_to_response(
        'home/404.html',
        {},
        context_instance=RequestContext(request)
    )

    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response(
        'home/500.html',
        {},
        context_instance=RequestContext(request)
    )

    response.status_code = 500
    return response
