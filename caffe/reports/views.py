from django.shortcuts import render
from django.contrib import messages

from .models import Report, FullProduct, Product, Unit, Category
from .forms import ReportForm

def reports_show_all_reports(request):
    reports = Report.objects.all()
    return render(request, 'reports/all.html', {'reports': reports})

def reports_create_new_report(request):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request)

    return render(request, 'reports/create.html', {'form': form})

def reports_show_report(request, report_id):
    report = Report.objects.get(id=report_id)

    # checks if report exists
    if not report:
        messages.error(request, 'Raport nie istnieje.')
        return redirect('reports.reports_show_all_reports')

    all_categories = {}
    fullProducts = report.full_products.all()

    for fullProduct in fullProducts:
        product = fullProduct.product
        category = product.category
        unit = product.unit

        # add product to specific category
        if category.name not in all_categories:
            all_categories[category.name] = []

        all_categories[category.name].append({
            'name': product.name,
            'amount': fullProduct.amount,
            'unit': unit.name
        })


    return render(request, 'reports/show.html', {
        'report': report,
        'categories': all_categories
    })
