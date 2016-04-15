from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Report, FullProduct, Product, Unit, Category
from .forms import ReportForm, ProductForm
from .forms import FullProductForm, UnitForm, CategoryForm

# url(r'^new/category/$', reports_new_category, name='reports_new_category'),
# url(r'^edit/category/(?P<category_id>\d+)/$',
# 	reports_edit_category, name='reports_edit_category'),
#
# url(r'^new/unit/$', reports_new_unit, name='reports_new_unit'),
# url(r'^edit/unit/(?P<unit_id>\d+)/$',
# 	reports_edit_unit, name='reports_edit_unit'),
#
# url(r'^new/product/$', reports_new_product, name='reports_new_product'),
# url(r'^edit/product/(?P<product_id>\d+)/$',
# 	reports_edit_product, name='reports_edit_product'),
#
# url(r'^new/fullproduct/$',
# 	reports_new_fullproduct, name='reports_new_fullproduct'),
# url(r'^edit/fullproduct/(?P<fullproduct_id>\d+)/$',
# 	reports_edit_fullproduct, name='reports_edit_fullproduct'),
#
# url(r'^new/report/$', reports_new_report, name='reports_new_report'),
# url(r'^edit/report/(?P<report_id>\d+)/$',
# 	reports_edit_report, name='reports_edit_report'),

def reports_new_category(request):
    elements = []
    form = CategoryForm()

    if request.POST:
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('reports_create'))

    categories = Category.objects.all()
    for category in categories:
        elements.append({
            'edit_href': reverse('reports_edit_category', args=(category.id,)),
            'id': category.id,
            'desc': str(category)
        })

    return render(request, 'reports/new_element.html', {
        'form': form,
        'context': {
            'title': "Nowa kategoria",
            'save_title': "Zapisz kategorię",
            'message': ""
        },
        'elements': elements
    })

def reports_edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect(reverse('reports_create'))

    return render(request, 'reports/edit_element.html', {
        'form': form,
        'context': {
            'title': "Edytuj kategorię",
            'save_title': "Uaktualnij kategorię"
        }
    })


def reports_new_unit(request):
    elements = []
    form = UnitForm()

    if request.POST:
        form = UnitForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('reports_create'))

    units = Unit.objects.all()
    for unit in units:
        elements.append({
            'edit_href': reverse('reports_edit_unit', args=(unit.id,)),
            'id': unit.id,
            'desc': str(unit)
        })

    return render(request, 'reports/new_element.html', {
        'form': form,
        'context': {
            'title': "Nowa jednostka",
            'save_title': "Zapisz jednostkę",
            'message': ""
        },
        'elements': elements
    })

def reports_edit_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    form = UnitForm(request.POST or None, instance=unit)

    if form.is_valid():
        form.save()
        return redirect(reverse('reports_create'))

    return render(request, 'reports/edit_element.html', {
        'form': form,
        'context': {
            'title': "Edytuj jednostkę",
            'save_title': "Uaktualnij jednostkę"
        }
    })


def reports_new_product(request):
    elements = []
    form = ProductForm()

    if request.POST:
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('reports_create'))

    products = Product.objects.all()
    for product in products:
        elements.append({
            'edit_href': reverse('reports_edit_product', args=(product.id,)),
            'id': product.id,
            'desc': str(product)
        })

    return render(request, 'reports/new_element.html', {
        'form': form,
        'context': {
            'title': "Nowy produkt",
            'save_title': "Zapisz produkt",
            'message': ""
        },
        'elements': elements
    })

def reports_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect(reverse('reports_create'))

    return render(request, 'reports/edit_element.html', {
        'form': form,
        'context': {
            'title': "Edytuj produkt",
            'save_title': "Uaktualnij produkt"
        }
    })

def reports_new_fullproduct(request):
    elements = []
    form = FullProductForm()

    if request.POST:
        form = FullProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('reports_create'))

    fullProducts = FullProduct.objects.all()
    for fullProduct in fullProducts:
        elements.append({
            'edit_href': reverse('reports_edit_fullproduct', args=(fullproduct.id,)),
            'id': fullProduct.id,
            'desc': str(fullProduct)
        })

    return render(request, 'reports/new_element.html', {
        'form': form,
        'context': {
            'title': "Nowy pełny produkt",
            'save_title': "Zapisz pełny produkt",
            'message': ""
        },
        'elements': elements
    })

def reports_edit_fullproduct(request, fullproduct_id):
    fullproduct = get_object_or_404(Unit, id=fullproduct_id)
    form = FullProductForm(request.POST or None, instance=fullproduct)

    if form.is_valid():
        form.save()
        return redirect(reverse('reports_create'))

    return render(request, 'reports/edit_element.html', {
        'form': form,
        'context': {
            'title': "Edytuj pełny produkt",
            'save_title': "Uaktualnij pełny produkt"
        }
    })

def reports_new_report(request):
    elements = []
    form = ReportForm()

    if request.POST:
        form = ReportForm(request.POST)

        if form.is_valid():
            report = form.save()
            for fullProduct in form.cleaned_data['full_products']:
                fullProduct.report = report
                fullProduct.save()

            return redirect(reverse('reports_create'))

    reports = Report.objects.all()
    for report in reports:
        elements.append({
            'edit_href': reverse('reports_edit_report', args=(report.id,)),
            'id': report.id,
            'desc': str(report)
        })

    return render(request, 'reports/new_element.html', {
        'form': form,
        'context': {
            'title': "Nowy raport",
            'save_title': "Zapisz raport",
            'message': ""
        },
        'elements': elements
    })

def reports_edit_report(request, report_id):
    report = get_object_or_404(Unit, id=report_id)
    form = ReportForm(request.POST or None, instance=report)

    if form.is_valid():
        form.save()
        return redirect(reverse('reports_create'))

    return render(request, 'reports/edit_element.html', {
        'form': form,
        'context': {
            'title': "Edytuj raport",
            'save_title': "Uaktualnij raport"
        }
    })


def reports_create(request):
    return render(request, 'reports/create.html')

def reports_show_all_reports(request):
    reports = Report.objects.all()
    return render(request, 'reports/all.html', {'reports': reports})


def reports_show_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

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
