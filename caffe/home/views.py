from django.shortcuts import render, render_to_response
from django.template import RequestContext

def caffe_navigate(request):
    """Show main page."""

    return render(request, 'home/caffe.html')


def handler404(request):
    """Show 404 page whenever 404 error occurs."""

    response = render_to_response(
        'home/404.html',
        {},
        context_instance=RequestContext(request)
    )

    response.status_code = 404
    return response


def handler500(request):
    """Show 500 page whenever 500 error occurs."""

    response = render_to_response(
        'home/500.html',
        {},
        context_instance=RequestContext(request)
    )

    response.status_code = 500
    return response
