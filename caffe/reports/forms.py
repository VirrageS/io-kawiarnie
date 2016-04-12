from django import forms
from .models import Report, Category, Unit, FullProduct, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'unit',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('name',)


class FullProductForm(forms.ModelForm):
    class Meta:
        model = FullProduct
        fields = ('product', 'amount',)


class ReportForm(forms.ModelForm):
    full_products = forms.MultipleChoiceField(queryset=
        FullProduct.objects.filter(report__isnull=True))

    class Meta:
        model = Report