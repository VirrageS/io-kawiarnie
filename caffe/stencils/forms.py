# -*- encoding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from reports.models import Category

from .models import Stencil


class StencilForm(forms.ModelForm):
    """Responsible for proper saving Stencil model."""

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.order_by('name'),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Stencil
        fields = ('name', 'description', 'categories',)

    def __init__(self, *args, **kwargs):
        """Initialize all necessary information of form."""

        self._caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')  # removes ":" from labels
        super(StencilForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['description'].label = 'Opis'
        self.fields['categories'].label = 'Kategorie'

        if self.instance.id:
            # set initially selected categories
            categories = self.instance.categories
            self.initial['categories'] = [
                category.id for category in categories.order_by('name')
            ]

    def save(self, commit=True):
        """Override the save method to add Caffe relation."""

        stencil = super(StencilForm, self).save(commit=False)
        stencil.caffe = self._caffe
        if commit:
            stencil.save()

        return stencil

    def clean_name(self):
        """Check name field."""

        name = self.cleaned_data['name']
        query = Stencil.objects.filter(name=name, caffe=self._caffe)
        if query.exists():
            raise ValidationError(_('Nazwa nie jest unikalna.'))

        return name
