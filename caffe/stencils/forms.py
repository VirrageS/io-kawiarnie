# -*- encoding: utf-8 -*-

from django import forms

from reports.models import Category

from .models import Stencil


class StencilForm(forms.ModelForm):
    """Responsible for proper saving Stencil model."""

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Stencil
        fields = ('name', 'description', 'categories',)

    def __init__(self, *args, **kwargs):
        """Initialize all necessarry informations of form."""

        kwargs.setdefault('label_suffix', '')  # removes ":" from labels
        super(StencilForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['description'].label = 'Opis'
        self.fields['categories'].label = 'Kategorie'

        if self.instance.id:
            # set initally selected categories
            self.initial['categories'] = [
                category.id for category in self.instance.categories.all()
            ]
