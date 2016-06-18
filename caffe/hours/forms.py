# -*- encoding: utf-8 -*-

from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Position, WorkedHours


class PositionForm(forms.ModelForm):
    """Responsible for checking Position model."""

    class Meta:
        model = Position
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Position's fields."""

        self._caffe = kwargs.pop('caffe')
        kwargs.setdefault('label_suffix', '')

        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'Nazwa'

        if self.instance.id:
            self.initial['name'] = self.instance.name

    def save(self, commit=True):
        """Override the save method to add Caffe relation."""

        position = super(PositionForm, self).save(commit=False)
        position.caffe = self._caffe
        if commit:
            position.save()

        return position

    def clean_name(self):
        """Check name field."""

        name = self.cleaned_data['name']
        query = Position.objects.filter(name=name, caffe=self._caffe)
        if query.exists():
            raise ValidationError(_('Name is not unique.'))

        return name


class WorkedHoursForm(forms.ModelForm):
    """Responsible for setting up WorkedHours model."""

    start_time = forms.TimeField(
        label=u'Godzina rozpoczęcia',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={'placeholder': '12:30'}
        ),
    )
    end_time = forms.TimeField(
        label=u'Godzina zakończenia',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={'placeholder': '12:30'}
        ),
    )
    date = forms.DateField(
        label=u'Dzień',
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={'placeholder': '22.03.2016'}
        ),
    )

    class Meta:
        model = WorkedHours
        fields = ('start_time', 'end_time', 'date', 'position')

    def __init__(self, *args, **kwargs):
        """Initialize all Worked Hours's fields."""

        kwargs.setdefault('label_suffix', '')
        self.employee = kwargs.pop('employee', None)

        super(WorkedHoursForm, self).__init__(*args, **kwargs)
        self.fields['position'].label = u'Stanowisko'

        if self.instance.id is None:
            self.initial['date'] = date.today()

    def clean(self):
        """Clean data and check validation."""

        cleaned_data = super(WorkedHoursForm, self).clean()

        cleaned_start_time = cleaned_data.get("start_time")
        cleaned_end_time = cleaned_data.get("end_time")
        cleaned_date = cleaned_data.get("date")

        if cleaned_start_time and cleaned_end_time and cleaned_date:
            intersect = WorkedHours.objects.filter(
                employee=self.employee,
                date=cleaned_date,
                start_time__lte=cleaned_end_time,
                end_time__gte=cleaned_start_time,
            )

            if self.instance.id:
                intersect = intersect.exclude(pk=self.instance.pk)

            if intersect.exists() > 0:
                self.add_error(
                    'date',
                    u'Godziny w danym dniu się nakładają.'
                )

            if cleaned_start_time > cleaned_end_time:
                self.add_error(
                    'start_time',
                    u'Czas rozpoczęcia jest później niż czas zakończenia.'
                )

    def save(self, commit=True):
        """Save WorkedHoursForm data to model."""

        hours = super(WorkedHoursForm, self).save(commit=False)
        hours.employee = self.employee
        hours.caffe = self.employee.caffe
        if commit:
            hours.save()

        return hours
