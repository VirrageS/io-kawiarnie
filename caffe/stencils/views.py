from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from reports.models import Product

from .forms import StencilForm
from .models import Stencil


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
    return render(request, 'stencils/edit_stencil.html')


def stencils_show_stencil(request, stencil_id):
    return render(request, 'stencils/show_stencil.html')


def stencils_show_all_stencils(request):
    stencils = Stencil.objects.all()
    return render(request, 'stencils/show_all_stencils.html', {
        'stencils': stencils
    })


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
        # print(request.POST)
        # full_products = request.POST.getlist('1')
        pass

    return render(request, 'stencils/new_report.html', {
        'stencil': stencil,
        'categories': all_categories
    })


def stencils_edit_report(request, report_id):
    return render(request, 'stencils/edit_report.html')


def stencils_create(request):
    return render(request, 'stencils/create_stencil.html')
