from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import WorkedHoursForm, PositionForm
from .models import WorkedHours, Position


def hours_edit_position(request, position_pk):
    """Edit Position with id.

    Args:
        position_pk: Pk of Position which we want to get.
    """

    position = get_object_or_404(Position, pk=position_pk)
    form = PositionForm(request.POST or None, instance=position)

    if form.is_valid():
        form.save()
        return redirect(reverse('caffe_navigate'))

    return render(request, 'hours/new_position.html', {
        'form': form,
        'title': 'Dodaj stanowisko',
        'button': 'Dodaj'
    })


def hours_new_position(request):
    """Create new Position."""

    form = PositionForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(reverse('caffe_navigate'))

    positions = Position.objects.all()
    all_positions = []
    for position in positions:
        all_positions.append({
            'desc': position.name,
            'edit_url': reverse('edit_position', args=(position.pk,))
        })

    return render(request, 'hours/new_position.html', {
        'form': form,
        'positions': all_positions,
        'title': 'Dodaj stanowisko',
        'button': 'Dodaj'
    })


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
def hours_edit_worked_hours(request, hours_pk):
    """Edit WorkedHours with id.

    Args:
        hours_id: Id of WorkedHours which we want to get.
    """

    worked_hours = get_object_or_404(WorkedHours, pk=hours_pk)
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
