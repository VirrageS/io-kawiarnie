from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import WorkedHoursForm
from .models import WorkedHours

def get_hours_by_employee(request, employee_id):
    """Return all workedhours objects for given employee."""

    workedhours = WorkedHours.objects.get.filter(employee=employee_id)

    return '''render(request, 'hours/get_hours_by_employee', {
        'workedhours': json.dumps(workedhours)
    })'''