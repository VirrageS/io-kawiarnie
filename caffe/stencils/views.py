from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from reports.forms import FullProductForm
from reports.models import Product, Report
from reports.views import get_report_categories

from .forms import StencilForm
from .models import Stencil


@permission_required('stencils.add_stencil')
def stencils_new_stencil(request):
    """Show form to create new stencil and show existing stencils."""

    form = StencilForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Szablon został poprawnie dodany.')
        return redirect(reverse('reports:navigate'))

    stencils = Stencil.objects.all()
    return render(request, 'stencils/new.html', {
        'form': form,
        'stencils': stencils
    })


@permission_required('stencils.change_stencil')
def stencils_edit_stencil(request, stencil_id):
    """Edit already existing stencil with stencil_id."""

    stencil = get_object_or_404(Stencil, id=stencil_id)
    form = StencilForm(request.POST or None, instance=stencil)

    if form.is_valid():
        form.save()
        messages.success(request, 'Szablon został poprawnie zmieniony.')
        return redirect(reverse('reports:navigate'))

    return render(request, 'stencils/edit.html', {
        'form': form,
        'stencil': stencil
    })


@permission_required('stencils.view_stencil')
def stencils_show_stencil(request, stencil_id):
    """Show stencil with stencil_id."""

    stencil = get_object_or_404(Stencil, id=stencil_id)
    categories = stencil.categories.all()

    return render(request, 'stencils/show.html', {
        'stencil': stencil,
        'categories': categories
    })


@permission_required('stencils.view_stencil')
def stencils_show_all_stencils(request):
    """Show all existing stencils."""

    stencils = Stencil.objects.all()
    return render(request, 'stencils/all.html', {
        'stencils': stencils
    })


@permission_required('reports.add_report')
def stencils_new_report(request, stencil_id):
    """Create new report from given stencil.

    Validate if report is correct by FullProduct validation. Check if report
    is not empty.
    """

    checked = []
    all_categories = []

    stencil = get_object_or_404(Stencil, id=stencil_id)
    categories = stencil.categories.all()

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
            messages.success(request, 'Raport został poprawnie dodany.')
            return redirect(reverse('stencils:all'))
        else:
            messages.error(
                request,
                u'Formularz został niepoprawnie wypełniony.'
            )

    # get last five reports
    latest_reports = Report.objects.all()[:5]
    for report in latest_reports:
        report.categories = get_report_categories(report.id)

    return render(request, 'stencils/new_report.html', {
        'stencil': stencil,
        'categories': all_categories,
        'checked': checked,
        'reports': latest_reports
    })
