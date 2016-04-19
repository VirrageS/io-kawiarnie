from django.shortcuts import render

def stencils_create(request):
    return render(request, 'stencils/create_stencil.html')

def stencils_new_stencil(request):
    return render(request, 'stencils/new_stencil.html')

def stencils_new_report(request):
    return render(request, 'stencils/new_report.html')

def stencils_show(request):
    return render(request, 'stencils/show.html')
