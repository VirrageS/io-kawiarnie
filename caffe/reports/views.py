# -*- encoding: utf-8 -*-

import json

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, FullProductForm, ProductForm, UnitForm
from .models import Category, FullProduct, Product, Report, Unit


def get_report_categories(report_id):
    """Return all categories with products for given Report.

    Args:
        report_id (int): Id of Report which we want to display.

    Returns:
        All categories with products for Report, or None if Report does not
        exists.
    """

    report = None
    try:
        report = Report.objects.filter(id=report_id).first()
    except:
        return None

    if not report:
        return None

    all_categories = {}
    for full_product in report.full_products.all():
        product = full_product.product
        category = product.category
        unit = product.unit

        # add product to specific category
        if category.name not in all_categories:
            all_categories[category.name] = []

        all_categories[category.name].append({
            'name': product.name,
            'amount': full_product.amount,
            'unit': unit.name
        })

    return all_categories


@permission_required('reports.add_category')
def reports_new_category(request):
    """Show form to create new Category and show existing Categories."""

    elements = []
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Kategoria został poprawnie dodana.')
        return redirect(reverse('reports_navigate'))

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
            'title': u'Nowa kategoria'
        },
        'elements': elements
    })


@permission_required('reports.change_category')
def reports_edit_category(request, category_id):
    """Show form to edit Category.

    Args:
        category_id (int): Id of Category which is edited.
    """

    category = get_object_or_404(Category, id=category_id)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        messages.success(request, 'Kategoria został poprawnie zmieniona.')
        return redirect(reverse('reports_navigate'))

    return render(request, 'reports/edit_element.html', {
        'form': form,
        'context': {
            'title': u'Edytuj kategorię',
            'cancel_href': reverse('reports_new_category')
        }
    })


@permission_required('reports.add_unit')
def reports_new_unit(request):
    """Show form to create new Unit and show already existing Units."""

    elements = []
    form = UnitForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Jednostka została poprawnie dodana.')
        return redirect(reverse('reports_navigate'))

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
            'title': "Nowa jednostka"
        },
        'elements': elements
    })


@permission_required('reports.change_unit')
def reports_edit_unit(request, unit_id):
    """Show form to edit Unit.

    Args:
        unit_id (int): Id of Unit which is edited.
    """

    unit = get_object_or_404(Unit, id=unit_id)
    form = UnitForm(request.POST or None, instance=unit)

    if form.is_valid():
        form.save()
        messages.success(request, 'Jednostka została poprawnie zmieniona.')
        return redirect(reverse('reports_navigate'))

    return render(request, 'reports/edit_element.html', {
        'form': form,
        'context': {
            'title': 'Edytuj jednostkę',
            'cancel_href': reverse('reports_new_unit')
        }
    })


@permission_required('reports.add_product')
def reports_new_product(request):
    """Show form to create new Product and show already existing Products."""

    elements = []
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Produkt został poprawnie dodany.')
        return redirect(reverse('reports_navigate'))

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
            'title': u'Nowy produkt'
        },
        'elements': elements
    })


@permission_required('reports.change_product')
def reports_edit_product(request, product_id):
    """Show form to edit Product.

    Args:
        product_id (int): Id of Product which is edited.
    """

    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        messages.success(request, 'Produkt został poprawnie zmieniony.')
        return redirect(reverse('reports_navigate'))

    return render(request, 'reports/edit_element.html', {
        'form': form,
        'context': {
            'title': u'Edytuj produkt',
            'cancel_href': reverse('reports_new_product')
        }
    })


@permission_required('reports.add_report')
def reports_new_report(request):
    """Show form to create new Report and show already existing Report."""

    all_products = []

    products = Product.objects.all()
    for product in products:
        all_products.append({
            'id': product.id,
            'name': product.name,
            'unit': product.unit.name,
            'category': {
                'id': product.category.id,
                'name': product.category.name
            },
            'selected': False,
            'amount': '',
            'errors': {}
        })

    if request.POST:
        post = request.POST.copy()
        forms = []
        valid = True

        post.pop('csrfmiddlewaretoken', None)

        # chcek validation and create form for each fullproduct
        for full_product in post:
            fp_list = post.getlist(full_product)
            form = FullProductForm({
                # sets product id and amount for fullproduct
                'product': fp_list[0],
                'amount': fp_list[1]
            })

            valid = valid & form.is_valid()

            # update products values
            product = next(
                (p for p in all_products if p['id'] == int(fp_list[0])),
                None
            )

            if product:
                product['selected'] = True
                product['amount'] = (fp_list[1] if form.is_valid() else '')
                product['errors'] = (
                    '' if form.is_valid() else form.errors['amount']
                )

            forms.append(form)

        # check if some form exists
        if len(forms) > 0 and valid:
            report = Report.objects.create(
                creator=request.user
            )

            # for each form save it with its report
            for form in forms:
                full_product = form.save()
                full_product.report = report
                full_product.save()

            report.save()
            return redirect(reverse('reports_navigate'))

    # get last five reports
    latest_reports = Report.objects.all()[:5]
    for report in latest_reports:
        report.categories = get_report_categories(report.id)

    return render(request, 'reports/new_report.html', {
        'title':  'Nowy raport',
        'button': 'Dodaj',
        'reports': latest_reports,
        'products': json.dumps(all_products)
    })


@permission_required('reports.change_report')
def reports_edit_report(request, report_id):
    """Show form to edit Report.

    Args:
        report_id (int): Id of Report which is edited.
    """

    report = get_object_or_404(Report, id=report_id)

    all_products = []

    products = Product.objects.all()
    for product in products:
        parsed_product = {
            'id': product.id,
            'name': product.name,
            'unit': product.unit.name,
            'category': {
                'id': product.category.id,
                'name': product.category.name
            },
            'selected': False,
            'amount': '',
            'errors': {}
        }

        # mark as selected products which are assigned to report
        full_product = FullProduct.objects.filter(
            report=report.id, product=product.id
        ).first()

        if full_product and (not request.POST):
            parsed_product['selected'] = True
            parsed_product['amount'] = full_product.amount

        all_products.append(parsed_product)

    if request.POST:
        post = request.POST.copy()
        forms = []
        valid = True

        post.pop('csrfmiddlewaretoken', None)

        # chcek validation and create form for each fullproduct
        for full_product in post:
            fp_list = post.getlist(full_product)
            form = FullProductForm({
                # sets product id and amount for fullproduct
                'product': fp_list[0],
                'amount': fp_list[1]
            })

            valid = valid & form.is_valid()

            product = next(
                (p for p in all_products if p['id'] == int(fp_list[0])),
                None
            )

            if product:
                product['selected'] = True
                product['amount'] = (fp_list[1] if form.is_valid() else '')
                product['errors'] = (
                    '' if form.is_valid() else form.errors['amount']
                )

            forms.append(form)

        # check if some form exists
        if len(forms) > 0 and valid:
            full_products = FullProduct.objects.filter(report=report.id).all()
            for full_product in full_products:
                full_product.delete()

            # for each form save it with its report
            for form in forms:
                full_product = form.save()
                full_product.report = report
                full_product.save()

            report.save()
            return redirect(reverse('reports_navigate'))

    return render(request, 'reports/new_report.html', {
        'title': 'Edytuj raport',
        'button': 'Uaktualnij',
        'products': json.dumps(all_products)
    })


@permission_required('reports.view_report')
def reports_show_report(request, report_id):
    """Show Report with all Categories, Products, Units and FullProducts.

    Args:
        report_id (int): Id of Report which have to be shown.
    """

    report = get_object_or_404(Report, id=report_id)

    return render(request, 'reports/show.html', {
        'report': report,
        'categories': get_report_categories(report.id)
    })


@permission_required('reports.view_report')
def reports_show_all_reports(request):
    """Show all existing Reports."""

    reports = Report.objects.all()
    return render(request, 'reports/all.html', {'reports': reports})


@permission_required('reports.view_report')
def reports_navigate(request):
    """Show navigation view for reports."""

    return render(request, 'home/reports.html')
