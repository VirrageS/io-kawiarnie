# -*- encoding: utf-8 -*-

from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm      
from .models import Employee
from django.contrib.auth import get_user_model


class EmployeeForm(UserCreationForm):
    """Responsible for proper saving Employee form."""

    telephone_number = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Employee
        fields = (
            'username',
            'first_name',
            'last_name',
            'telephone_number',
            'email', 
            'favorite_coffee'
        )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # removes ":" from labels

        super(EmployeeForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['first_name'].label = 'Imię'
        self.fields['last_name'].label = 'Nazwisko'
        self.fields['telephone_number'].label = 'Numer telefonu'
        self.fields['email'].label = 'Adres email'
        self.fields['favorite_coffee'].label = 'Twoja ulubiona kawa?'

        if self.instance:
            self.initial['username'] = self.instance.username
            self.initial['first_name'] = self.instance.first_name
            self.initial['last_name'] = self.instance.last_name
            self.initial['telephone_number'] = self.instance.telephone_number
            self.initial['email'] = self.instance.email
            self.initial['favorite_coffee'] = self.instance.favorite_coffee

