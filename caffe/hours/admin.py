from django.contrib import admin

from .models import WorkedHours, Position

# Register your models here.

admin.site.register(WorkedHours)
admin.site.register(Position)
