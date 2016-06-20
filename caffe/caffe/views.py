from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from employees.forms import EmployeeForm

from .forms import CaffeForm


def index_navigate(request):
    """Show main page."""

    if request.user.is_authenticated():
        return redirect(reverse('home:navigate'))

    return render(request, 'home/landing_page.html')


def caffe_create(request):
    """Create caffe view."""

    caffe_form = CaffeForm(request.POST or None)
    admin_form = EmployeeForm(request.POST or None, caffe=None)

    if caffe_form.is_valid() and admin_form.is_valid():
        caffe = caffe_form.save()
        admin = admin_form.save(commit=False)
        admin.caffe = caffe
        admin.save()

        group = Group.objects.get(name='Admin')
        admin.groups.add(group)

        messages.success(
            request,
            'Kawiarnia i użytkownika zostały poprawnie utworzone.'
        )
        return redirect(reverse('employees:login'))
    elif request.POST:
        messages.error(request, u'Formularz został niepoprawnie wypełniony.')

    return render(request, 'caffe/new.html', {
        'caffe_form': caffe_form,
        'admin_form': admin_form,
    })
