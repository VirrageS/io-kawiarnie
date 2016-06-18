from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render


def index_navigate(request):
    """Show main page."""

    if request.user.is_authenticated():
        return redirect(reverse('caffe_navigate'))

    return render(request, 'home/landing_page.html')
