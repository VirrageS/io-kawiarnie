# -*- encoding: utf-8 -*-

from django import forms
from .models import Stencil
from reports.models import Category

class StencilForm(forms.ModelForm):
    class Meta:
        model = Stencil
        fields = ('name', 'categories',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(StencilForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['categories'].label = 'Kategorie'
        self.fields['categories'].queryset = Category.objects.all()

        if self.instance.id:
            self.initial['categories'] = [c.id for c in self.instance.categories.all()]
