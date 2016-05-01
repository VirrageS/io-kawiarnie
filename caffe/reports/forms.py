"""Forms for setting up elements of a report and report itself."""

# -*- encoding: utf-8 -*-

from django import forms

from .models import Category, FullProduct, Product, Report, Unit


class ProductForm(forms.ModelForm):
    """Responsible for setting up a Product."""

    class Meta:
        model = Product
        fields = ('name', 'category', 'unit',)

    def __init__(self, *args, **kwargs):
        """Initializes all Product's fields."""

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
        """Initializes all Category's fields."""

        kwargs.setdefault('label_suffix', '')
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'


class UnitForm(forms.ModelForm):
    """Responsible for setting up a Unit."""

    class Meta:
        model = Unit
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initializes all Unit's fields."""

        kwargs.setdefault('label_suffix', '')
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'


class FullProductForm(forms.ModelForm):
    """Responsible for setting up a FullProduct - Product with its amount."""

    class Meta:
        model = FullProduct
        fields = ('product', 'amount',)

    def __init__(self, *args, **kwargs):
        """Initializes all FullProduct's fields."""

        kwargs.setdefault('label_suffix', '')
        super(FullProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].label = 'Produkt'
        self.fields['amount'].label = u'Ilość'
        self.fields['product'].empty_label = None


class ReportForm(forms.ModelForm):
    """Responsible for setting up a Report."""

    full_products = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        """Initializes all Report's fields."""

        kwargs.setdefault('label_suffix', '')
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['full_products'].label = u'Pełne produkty'
        self.fields['full_products'].queryset = \
            FullProduct.objects.filter(report__isnull=True)

        # In case of editing, formerly picked FullProducts are added to
        # available options.
        if self.instance.id:
            instance_fullproducts = \
                FullProduct.objects.filter(report=self.instance.id)

            self.fields['full_products'].queryset |= instance_fullproducts
            self.initial['full_products'] = instance_fullproducts

    class Meta:
        model = Report
        fields = '__all__'
