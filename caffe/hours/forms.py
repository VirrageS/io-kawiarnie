# -*- encoding: utf-8 -*-

from datetime import date

from django import forms

from .models import Position, WorkedHours


class PositionForm(forms.ModelForm):
    """Responsible for checking Position model."""

    class Meta:
        model = Position
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Position's fields."""

        kwargs.setdefault('label_suffix', '')

        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'Nazwa'

        if self.instance.id:
            self.initial['name'] = self.instance.name


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

        if self.instance.id:
            self.initial['start_time'] = self.instance.start_time
            self.initial['end_time'] = self.instance.end_time
            self.initial['date'] = self.instance.date
        else:
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
                end_time__gte=cleaned_start_time
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
