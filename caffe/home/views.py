from datetime import date

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from cash.models import CashReport
from hours.models import WorkedHours
from reports.models import Report


@permission_required(['hours.view_workedhours', 'reports.view_report',
                      'cash.view_cashreport'])
def caffe_navigate(request):
    """Show caffe main page."""

    year = date.today().year
    month = date.today().month
    day = date.today().day

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

    return render(request, 'home/caffe.html', {
        'reports': reports,
        'cash_reports': cash_reports,
        'worked_hours': worked_hours
    })


# def handler404(request):
#     """Show 404 page whenever 404 error occurs."""
#
#     response = render_to_response(
#         'home/404.html',
#         {},
#         context_instance=RequestContext(request)
#     )
#
#     response.status_code = 404
#     return response
#
#
# def handler500(request):
#     """Show 500 page whenever 500 error occurs."""
#
#     response = render_to_response(
#         'home/500.html',
#         {},
#         context_instance=RequestContext(request)
#     )
#
#     response.status_code = 500
#     return response
