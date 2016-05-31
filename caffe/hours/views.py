from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import WorkedHoursForm
from .models import WorkedHours


@permission_required('hours.view_workedhours')
def hours_get_day_worked_hours(request, day, month, year):
    """Get all WorkedHours from particular day.

    Args:
        day: Day from which we want to get WorkedHours.
        month: Month from which we want to get WorkedHours.
        year: Year from which we want to get WorkedHours.
    """

    worked_hours_day = WorkedHours.objects.filter(
        created_on__year=year,
        created_on__month=month,
        created_on__day=day
    ).all()

    worked_hours = []
    for worked_hour in worked_hours_day:
        worked_hours.append(worked_hour.serialize())

    return JsonResponse(worked_hours)


@permission_required('hours.add_workedhours')
def hours_new_worked_hours(request):
    """Create new WorkedHours."""

    form = WorkedHoursForm(request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': 'Poprawnie dodano przepracowane godziny.'
        })

    return JsonResponse({'errors': form.errors})


@permission_required('hours.edit_workedhours')
def hours_edit_worked_hours(request, hours_id):
    """Edit WorkedHours with id.

    Args:
        hours_id: Id of WorkedHours which we want to get.
    """

    worked_hours = get_object_or_404(WorkedHours, id=hours_id)
    form = WorkedHoursForm(request.POST, instance=worked_hours)

    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': 'Poprawnie edytowano przepracowane godziny.'
        })

    return JsonResponse({'errors': form.errors})


@permission_required('hours.view_workedhours')
def hours_get_worked_hours(request, hours_id):
    """Get WorkedHours with id.

    Args:
        hours_id: Id of WorkedHours which we want to get.
    """

    worked_hours = get_object_or_404(WorkedHours, id=hours_id)
    return JsonResponse(worked_hours.serialize())
