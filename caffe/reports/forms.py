# -*- encoding: utf-8 -*-

from django import forms
from .models import Report, Category, Unit, FullProduct, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'unit',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['category'].label = 'Kategoria'
        self.fields['unit'].label = 'Jednostka'
        self.fields['category'].empty_label = None
        self.fields['unit'].empty_label = None


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'


class FullProductForm(forms.ModelForm):
    class Meta:
        model = FullProduct
        fields = ('product', 'amount',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(FullProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].label = 'Produkt'
        self.fields['amount'].label = u'Ilość'
        self.fields['product'].empty_label = None


class ReportForm(forms.ModelForm):
    full_products = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['full_products'].label = u'Pełne produkty'
        self.fields['full_products'].queryset = \
            FullProduct.objects.filter(report__isnull=True)

        if self.instance.id:
            instance_fullproducts = \
                FullProduct.objects.filter(report=self.instance.id)

            self.fields['full_products'].queryset |= instance_fullproducts
            self.initial['full_products'] = instance_fullproducts

    class Meta:
        model = Report
        fields = '__all__'
