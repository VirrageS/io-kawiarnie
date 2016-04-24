from django.contrib import admin

from .models import Category, FullProduct, Product, Report, Unit

admin.site.register(Report)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Unit)
admin.site.register(FullProduct)
