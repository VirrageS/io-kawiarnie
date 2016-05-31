from django.shortcuts import render

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import WorkedHoursForm
from .models import WorkedHours

# Create your views here.
