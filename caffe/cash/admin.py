from django.contrib import admin

from .models import CashReport, Company, Expense

admin.site.register(CashReport)
admin.site.register(Company)
admin.site.register(Expense)
