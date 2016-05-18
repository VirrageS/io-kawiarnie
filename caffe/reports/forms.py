# -*- encoding: utf-8 -*-

from django import forms

from .models import Category, FullProduct, Product, Report, Unit


class ProductForm(forms.ModelForm):
    """Responsible for setting up a Product."""

    class Meta:
        model = Product
        fields = ('name', 'category', 'unit',)

    def __init__(self, *args, **kwargs):
        """Initialize all Product's fields."""

        kwargs.setdefault('label_suffix', '')
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['category'].label = 'Kategoria'
        self.fields['unit'].label = 'Jednostka'
        self.fields['category'].empty_label = None
        self.fields['unit'].empty_label = None


class CategoryForm(forms.ModelForm):
    """Responsible for setting up a Category."""

    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Category's fields."""

        kwargs.setdefault('label_suffix', '')
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'


class UnitForm(forms.ModelForm):
    """Responsible for setting up a Unit."""

    class Meta:
        model = Unit
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Unit's fields."""

        kwargs.setdefault('label_suffix', '')
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'


class FullProductForm(forms.ModelForm):
    """Responsible for setting up a FullProduct - Product with its amount."""

    class Meta:
        model = FullProduct
        fields = ('product', 'amount',)

    def __init__(self, *args, **kwargs):
        """Initialize all FullProduct's fields."""

        kwargs.setdefault('label_suffix', '')
        super(FullProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].label = 'Produkt'
        self.fields['amount'].label = u'Ilość'
        self.fields['product'].empty_label = None
