# -*- encoding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Category, FullProduct, Product, Report, Unit


class ProductForm(forms.ModelForm):
    """Responsible for setting up a Product."""

    class Meta:
        model = Product
        fields = ('name', 'category', 'unit',)

    def __init__(self, *args, **kwargs):
        """Initialize all Product's fields."""

        self._caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['category'].label = 'Kategoria'
        self.fields['unit'].label = 'Jednostka'
        self.fields['category'].empty_label = None
        self.fields['unit'].empty_label = None

    def clean_name(self):
        """Check name field."""

        name = self.cleaned_data['name']
        query = Product.objects.filter(name=name, caffe=self._caffe)

        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise ValidationError(_('Nazwa nie jest unikalna.'))

        return name

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        product = super(ProductForm, self).save(commit=False)
        product.caffe = self._caffe
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

        self._caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'

    def clean_name(self):
        """Check name field."""

        name = self.cleaned_data['name']

        query = Category.objects.filter(name=name, caffe=self._caffe)

        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise ValidationError(_('Nazwa nie jest unikalna.'))

        return name

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        category = super(CategoryForm, self).save(commit=False)
        category.caffe = self._caffe
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

        self._caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'

    def clean_name(self):
        """Check name field."""

        name = self.cleaned_data['name']
        query = Unit.objects.filter(name=name, caffe=self._caffe)

        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise ValidationError(_('Nazwa nie jest unikalna.'))

        return name

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        unit = super(UnitForm, self).save(commit=False)
        unit.caffe = self._caffe
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

        self._caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(FullProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].label = 'Produkt'
        self.fields['amount'].label = u'Ilość'
        self.fields['product'].empty_label = None

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        full_product = super(FullProductForm, self).save(commit=False)
        full_product.caffe = self._caffe
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

        self._caffe = kwargs.pop('caffe')
        self._creator = kwargs.pop('creator')

        kwargs.setdefault('label_suffix', '')
        super(ReportForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        report = super(ReportForm, self).save(commit=False)
        report.caffe = self._caffe
        report.creator = self._creator
        if commit:
            report.save()

        return report
