from django.shortcuts import render

def reports_show_all_reports(request):
    return render(request, 'reports/all.html')

def reports_create_new_report(request):
    return render(request, 'reports/create.html')
