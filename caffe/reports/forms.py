# -*- encoding: utf-8 -*-

from django import forms

from .models import Category, FullProduct, Product, Unit, Report


class ProductForm(forms.ModelForm):
    """Responsible for setting up a Product."""

    class Meta:
        model = Product
        fields = ('name', 'category', 'unit',)

    def __init__(self, *args, **kwargs):
        """Initialize all Product's fields."""

        self.caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['category'].label = 'Kategoria'
        self.fields['unit'].label = 'Jednostka'
        self.fields['category'].empty_label = None
        self.fields['unit'].empty_label = None

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        product = super(ProductForm, self).save(commit=False)
        product.caffe = self.caffe
        if commit:
            product.save()

        return product


class CategoryForm(forms.ModelForm):
    """Responsible for setting up a Category."""

    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Category's fields."""

        self.caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        category = super(CategoryForm, self).save(commit=False)
        category.caffe = self.caffe
        if commit:
            category.save()

        return category

class UnitForm(forms.ModelForm):
    """Responsible for setting up a Unit."""

    class Meta:
        model = Unit
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Unit's fields."""

        self.caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        unit = super(UnitForm, self).save(commit=False)
        unit.caffe = self.caffe
        if commit:
            unit.save()

        return unit


class FullProductForm(forms.ModelForm):
    """Responsible for setting up a FullProduct - Product with its amount."""

    class Meta:
        model = FullProduct
        fields = ('product', 'amount',)

    def __init__(self, *args, **kwargs):
        """Initialize all FullProduct's fields."""

        self.caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(FullProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].label = 'Produkt'
        self.fields['amount'].label = u'Ilość'
        self.fields['product'].empty_label = None

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        full_product = super(CategoryForm, self).save(commit=False)
        full_product.caffe = self.caffe
        if commit:
            full_product.save()

        return full_product


class ReportForm(forms.ModelForm):
    """Responsible for setting up a Report."""

    class Meta:
        model = Report
        fields = ()

    def __init__(self, *args, **kwargs):
        """Initialize all ReportForm's fields."""

        self.caffe = kwargs.pop('caffe')
        self.employee = kwargs.pop('employee')

        kwargs.setdefault('label_suffix', '')
        super(ReportForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        report = super(ReportForm, self).save(commit=False)
        report.caffe = self.caffe
        report.creator = self.employee
        if commit:
            report.save()

        return report
