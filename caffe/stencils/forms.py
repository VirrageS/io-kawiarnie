# -*- encoding: utf-8 -*-

from django import forms

from reports.models import Category

from .models import Stencil


class StencilForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Stencil
        fields = ('name', 'description', 'categories',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(StencilForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['description'].label = 'Opis'
        self.fields['categories'].label = 'Kategorie'

        if self.instance.id:
            self.initial['categories'] = [
                category.id for category in self.instance.categories.all()
            ]
