from django.shortcuts import render

from reports.models import Report


def calendar_navigate(request):
    """Show calendar."""

    return render(request, 'home/calendar.html')


def calendar_show_day(request, day):
    """Show day."""

    reports = Report.objects.all()

    return render(request, 'calendar/day.html')
