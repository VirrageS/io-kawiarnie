from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from reports.forms import FullProductForm
from reports.models import Product, Report
from reports.views import get_report_categories

from .forms import StencilForm
from .models import Stencil


def stencils_new_stencil(request):
    """Show form to create new stencil and show existing stencils."""

    final_stencils = []
    form = StencilForm()

    if request.POST:
        form = StencilForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('stencils_create'))

    stencils = Stencil.objects.order_by('name')
    for stencil in stencils:
        final_stencils.append({
            'edit_href': reverse('stencils_edit_stencil', args=(stencil.id,)),
            'show_href': reverse('stencils_show_stencil', args=(stencil.id,)),
            'id': stencil.id,
            'desc': str(stencil)
        })

    return render(request, 'stencils/new_stencil.html', {
        'form': form,
        'stencils': final_stencils
    })


def stencils_edit_stencil(request, stencil_id):
    """Edit already existing stencil with stencil_id."""
    stencil = get_object_or_404(Stencil, id=stencil_id)
    form = StencilForm(request.POST or None, instance=stencil)

    if form.is_valid():
        form.save()
        return redirect(reverse('stencils_create'))

    return render(request, 'stencils/edit_stencil.html', {
        'form': form,
        'stencil': stencil
    })


def stencils_show_stencil(request, stencil_id):
    """Show stencil with stencil_id."""
    stencil = get_object_or_404(Stencil, id=stencil_id)
    categories = stencil.categories.order_by('name')

    return render(request, 'stencils/show.html', {
        'stencil': stencil,
        'categories': categories
    })


def stencils_show_all_stencils(request):
    """Show all existing stencils."""
    stencils = Stencil.objects.order_by('name')
    return render(request, 'stencils/all.html', {
        'stencils': stencils
    })

def stencils_new_report(request, stencil_id):
    """Create new report from given stencil
    validation is correct if FullProduct validation is and
    report is not empty.
    """

    checked = []
    all_categories = []

    stencil = get_object_or_404(Stencil, id=stencil_id)
    categories = stencil.categories.order_by('name')

    for category in categories:
        products = Product.objects.filter(category=category).all()

        all_products = []
        for product in products:
            all_products.append({
                'id': product.id,
                'name': product.name,
                'unit': product.unit.name
            })

        all_categories.append({
            'id': category.id,
            'name': category.name,
            'products': all_products
        })

    if request.POST:
        full_products = request.POST
        forms = []
        valid = True

        # chcek validation and create form for each fullproduct
        for full_product in full_products:
            # csrf token ignore
            if full_product == 'csrfmiddlewaretoken':
                continue

            fp_list = full_products.getlist(full_product)
            form = FullProductForm({
                # sets product id and amount for fullproduct
                'product': fp_list[0],
                'amount': fp_list[1]
            })

            if not form.is_valid():
                valid = False
                checked.append({
                    'product': fp_list[0],
                    'amount': '',
                    'error': form.errors['amount']
                })
            else:
                checked.append({
                    'product': fp_list[0],
                    'amount': fp_list[1],
                    'error': ''
                })

            forms.append(form)

        # check if some form exists
        if len(forms) > 0 and valid:
            report = Report.objects.create()

            # for each form save it with its report
            for form in forms:
                full_product = form.save()
                full_product.report = report
                full_product.save()

            report.save()

            return redirect(reverse('stencils_show_all_stencils'))

    # get last five reports
    latest_reports = Report.objects.order_by('-created_on')[:5]
    for report in latest_reports:
        report.categories = get_report_categories(report.id)

    return render(request, 'stencils/new_report.html', {
        'stencil': stencil,
        'categories': all_categories,
        'checked': checked,
        'reports': latest_reports
    })


def stencils_create(request):
    """Render create_stencil."""
    return render(request, 'stencils/create_stencil.html')
