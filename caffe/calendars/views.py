import datetime

from django.shortcuts import render

from hours.models import WorkedHours
from reports.models import Report


def calendar_navigate(request):
    """Show calendar."""

    return render(request, 'home/calendar.html')


def calendar_show_day(request, day, month, year):
    """Show day."""

    reports = Report.objects.filter(
        created_on__year=year,
        created_on__month=month,
        created_on__day=day
    ).all()

    worked_hours = WorkedHours.objects.filter(
        date__year=year,
        date__month=month,
        date__day=day
    ).all()

    return render(request, 'calendar/day.html', {
        'reports': reports,
        'worked_hours': worked_hours,
        'date': {
            'year': year,
            'month': month,
            'day': day
        }
    })
