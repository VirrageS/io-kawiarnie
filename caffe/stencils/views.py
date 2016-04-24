from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django import forms

from reports.models import Product, Report, FullProduct

from .forms import StencilForm
from .models import Stencil
from reports.forms import FullProductForm


def stencils_new_stencil(request):
    final_stencils = []
    form = StencilForm()

    if request.POST:
        form = StencilForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('stencils_create'))

    stencils = Stencil.objects.all()
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
    stencil = get_object_or_404(Stencil, id=stencil_id)
    categories = stencil.categories.all()

    return render(request, 'stencils/show_stencil.html', {
        'stencil': stencil,
        'categories': categories
    })


def stencils_show_all_stencils(request):
    stencils = Stencil.objects.all()
    return render(request, 'stencils/show_all_stencils.html', {
        'stencils': stencils
    })

@csrf_exempt
def stencils_new_report(request, stencil_id):
    stencil = get_object_or_404(Stencil, id=stencil_id)
    categories = stencil.categories.all()

    all_categories = []
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

        for full_product in full_products:
            fp_list = full_products.getlist(full_product)
            form = FullProductForm({
                'product': fp_list[0],
                'amount': fp_list[1]
            })

            if not form.is_valid():
                return render(request, 'stencils/new_report.html', {
                    'stencil': stencil,
                    'categories': all_categories
                })

            forms.append(form)


        report = Report.objects.create()

        for form in forms:
            fp = form.save() 
            fp.report = report
            fp.save()

        report.save()

    return render(request, 'stencils/new_report.html', {
        'stencil': stencil,
        'categories': all_categories
    })


def stencils_edit_report(request, report_id):
    return render(request, 'stencils/edit_report.html')


def stencils_create(request):
    return render(request, 'stencils/create_stencil.html')
