import datetime

from django.shortcuts import render

from reports.models import Report
from cash.models import CashReport


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

    cash_reports = CashReport.objects.filter(
        created_on__year=year,
        created_on__month=month,
        created_on__day=day
    ).all()


    return render(request, 'calendar/day.html', {
        'reports': reports,
        'cash_reports': cash_reports,
        'date': {
            'year': year,
            'month': month,
            'day': day
        }
    })
