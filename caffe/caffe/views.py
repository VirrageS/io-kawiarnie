from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


def index_navigate(request):
    """Show main page."""

    if request.user.is_authenticated():
        return redirect(reverse('caffe_navigate'))

    return render(request, 'home/landing_page.html')
