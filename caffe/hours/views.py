# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PositionForm, WorkedHoursForm
from .models import Position, WorkedHours


@permission_required('hours.change_position')
def hours_edit_position(request, position_pk):
    """Edit Position with id.

    Args:
        position_pk: Pk of Position which we want to get.
    """

    position = get_object_or_404(
        Position,
        pk=position_pk,
        caffe=request.user.caffe
    )

    form = PositionForm(
        request.POST or None,
        instance=position,
        caffe=request.user.caffe
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Stanowisko zostało poprawnie zmienione.')
        return redirect(reverse('employees:navigate'))

    return render(request, 'hours/new_position.html', {
        'form': form,
        'title': u'Edytuj stanowisko',
        'button': u'Uaktualnij'
    })


@permission_required('hours.add_position')
def hours_new_position(request):
    """Create new Position."""

    form = PositionForm(request.POST or None, caffe=request.user.caffe)

    if form.is_valid():
        form.save()
        messages.success(request, 'Stanowisko zostało poprawnie utworzone.')
        return redirect(reverse('employees:navigate'))

    positions = Position.objects.filter(caffe=request.user.caffe).all()
    all_positions = []
    for position in positions:
        all_positions.append({
            'id': position.id,
            'desc': position.name
        })

    return render(request, 'hours/new_position.html', {
        'form': form,
        'positions': all_positions,
        'title': u'Nowe stanowisko',
        'button': u'Dodaj'
    })


@permission_required('hours.add_workedhours')
def hours_new_worked_hours(request):
    """Create new WorkedHours."""

    form = WorkedHoursForm(
        request.POST or None,
        employee=request.user,
        caffe=request.user.caffe
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Przepracowane godziny zostały poprawnie dodane.'
        )

        return redirect(reverse('home:navigate'))

    return render(request, 'hours/new.html', {
        'form': form,
        'title': u'Nowe przepracowane godziny',
        'button': u'Dodaj'
    })


@permission_required('hours.change_workedhours')
def hours_edit_worked_hours(request, hours_pk):
    """Edit WorkedHours with pk.

    Args:
        hours_pk: Pk of WorkedHours which we want to get.
    """

    worked_hours = get_object_or_404(
        WorkedHours,
        pk=hours_pk,
        caffe=request.user.caffe
    )

    if ((worked_hours.employee != request.user) and
            (not request.user.has_perm('hours.change_all_workedhours'))):
        raise Http404(u'Nie możesz edytować tych godzin.')

    form = WorkedHoursForm(
        request.POST or None,
        employee=worked_hours.employee,
        caffe=request.user.caffe,
        instance=worked_hours
    )

    if form.is_valid():
        form.save()
        messages.success(
            request,
            'Przepracowane godziny zostały poprawnie zmienione.'
        )

        return redirect(reverse('home:navigate'))

    return render(request, 'hours/new.html', {
        'form': form,
        'title': u'Edytuj przepracowane godziny',
        'button': u'Uaktualnij'
    })
