# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.models import \
    User, Group   # fill in custom user info then save it     
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Employee


class EmployeeForm(UserCreationForm):
    """Responsible for proper saving Employee form."""

    telephone_number = forms.CharField()
    email = forms.EmailField()

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Employee
        fields = (
            'username',
            'first_name',
            'last_name',
            'groups',
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
        self.fields['groups'].label = 'Grupy uprawnień użytkownika'

        self.fields['groups'].queryset |= Group.objects.all()

        if self.instance:
            self.initial['username'] = self.instance.username
            self.initial['first_name'] = self.instance.first_name
            self.initial['last_name'] = self.instance.last_name
            self.initial['telephone_number'] = self.instance.telephone_number
            self.initial['email'] = self.instance.email
            self.initial['favorite_coffee'] = self.instance.favorite_coffee
            
            try: 
                self.initial['groups'] = self.instance.group.get()
            except:
                # no groups
                pass

    def save(self, commit=True):
        instance = super(EmployeeForm, self).save(commit=False)
        
        # clear groups of user
        if instance.groups.all():
            instance.groups.clear()

        # add groups to user
        for g in self.cleaned_data['groups']:
            instance.groups.add(g)

        if commit:
            instance.save()

        return instance
