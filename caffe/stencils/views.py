from django.shortcuts import render

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


def stencils_new_report(request):
    return render(request, 'stencils/new_report.html')


def stencils_edit_report(request, report_id):
    return render(request, 'stencils/edit_report.html')


def stencils_create(request):
    return render(request, 'stencils/create_stencil.html')
