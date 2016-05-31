from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import WorkedHoursForm
from .models import WorkedHours

@permission_required('hours.add_workedhours')
def hours_new_worked_hours(request):
    """Create new WorkedHours."""

    form = WorkedHoursForm(request.POST or None, employee=request.user)

    if form.is_valid():
        hours = form.save(commit=False)
        hours.employee = request.user
        hours.save()
        return redirect(reverse('caffe_navigate'))

    return render(request, 'hours/new_hours.html', {
        'form': form,
        'title': 'Dodaj przepracowane godziny',
        'button': 'Dodaj'
    })


@permission_required('hours.edit_workedhours')
def hours_edit_worked_hours(request, hours_id):
    """Edit WorkedHours with id.

    Args:
        hours_id: Id of WorkedHours which we want to get.
    """

    worked_hours = get_object_or_404(WorkedHours, id=hours_id)
    form = WorkedHoursForm(request.POST or None, employee=request.user, instance=worked_hours)

    if form.is_valid():
        hours = form.save(commit=False)
        hours.employee = request.user
        hours.save()

        return redirect(reverse('caffe_navigate'))

    return render(request, 'hours/new_hours.html', {
        'form': form,
        'title': 'Edytuj przepracowane godziny',
        'button': 'Uaktulanij'
    })
