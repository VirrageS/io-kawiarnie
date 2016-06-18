# -*- encoding: utf-8 -*-

from django import forms

from .models import Caffe

import re

class CaffeForm(forms.ModelForm):
    """Responsible for setting up a Caffe."""
    house_number = forms.CharField(required=False)

    class Meta:
        model = Caffe
        fields = (
            'name',
            'city',
            'street',
            'postal_code',
            'building_number',
            'house_number'
        )

    def __init__(self, *args, **kwargs):
        """Initialize all Caffe's fields."""

        kwargs.setdefault('label_suffix', '')

        super(CaffeForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'Nazwa kawiarnii'
        self.fields['city'].label = u'Miasto'
        self.fields['street'].label = u'Ulica'
        self.fields['postal_code'].label = u'Kod pocztowy'
        self.fields['building_number'].label = u'Numer budynku'
        self.fields['house_number'].label = u'Numer lokalu'

        if self.instance:
            self.initial['name'] = self.instance.name
            self.initial['city'] = self.instance.city
            self.initial['street'] = self.instance.street
            self.initial['postal_code'] = self.instance.postal_code
            self.initial['building_number'] = self.instance.building_number
            self.initial['house_number'] = self.instance.house_number

    def clean(self):
        """Clean data and check validation."""

        cleaned_data = super(CaffeForm, self).clean()
        cleaned_postal_code = cleaned_data.get("postal_code")

        postal_pattern = re.compile('^[0-9]{2}-?[0-9]{3}$')

        if not cleaned_postal_code or \
           not postal_pattern.match(cleaned_postal_code):
            self.add_error(
                'postal_code',
                u'Kod pocztowy musi być w formacie liczbowym XX-XXX.'
            )
