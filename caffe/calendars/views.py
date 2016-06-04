from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from cash.models import CashReport
from hours.models import WorkedHours
from reports.models import Report


@login_required
def calendar_navigate(request):
    """Show calendar."""

    return render(request, 'home/calendar.html')


@permission_required('hours.view_workedhours', 'reports.view_report',
                     'cash.view_cashreport')
def calendar_show_day(request, year, month, day):
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

    worked_hours = WorkedHours.objects.filter(
        date__year=year,
        date__month=month,
        date__day=day
    ).all()

    return render(request, 'calendar/day.html', {
        'reports': reports,
        'cash_reports': cash_reports,
        'worked_hours': worked_hours,
        'date': {
            'year': year,
            'month': month,
            'day': day
        }
    })
