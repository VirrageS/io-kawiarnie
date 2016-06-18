from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

# from .forms import CaffeForm
from employees.forms import EmployeeForm


def index_navigate(request):
    """Show main page."""

    if request.user.is_authenticated():
        return redirect(reverse('caffe_navigate'))

    return render(request, 'home/landing_page.html')


def caffe_create(request):
    """Create caffe view."""

    # caffe_form = CaffeForm(request.POST or None)
    # admin_form = EmployeeForm(request.POST or None)
    #
    # if caffe_form.is_valid() and admin_form.is_valid():
    #     caffe = caffe_form.save()
    #     admin = admin_form.save(commit=False)
    #     admin.caffe_id = caffe.id
    #     admin.save()
    #
    #     return render(reverse('login_employee'))

    return render(request, 'caffe/add_caffe.html', {
        # 'caffe_form': caffe_form,
        # 'admin_form': admin_form,
    })
