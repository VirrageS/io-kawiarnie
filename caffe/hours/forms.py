from datetime import date

from django import forms
from .models import WorkedHours, Position

class PositionForm(forms.ModelForm):
    """Responsible for checking Position model."""

    class Meta:
        model = Position
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Position's fields."""

        kwargs.setdefault('label_suffix', '')

        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'

        if self.instance.id:
            self.initial['name'] = self.instance.name

class WorkedHoursForm(forms.ModelForm):
    """Responsible for setting up WorkedHours model."""
    start_time = forms.TimeField(
        label='Godzina rozpoczęcia',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={'placeholder': '12:30'}
        ),
    )
    end_time = forms.TimeField(
        label='Godzina zakończenia',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={'placeholder': '12:30'}
        ),
    )
    date = forms.DateField(
        label='Dzień',
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
        self.fields['position'].label = 'Stanowisko'

        if self.instance.id:
            self.initial['start_time'] = self.instance.start_time
            self.initial['end_time'] = self.instance.end_time
            self.initial['date'] = self.instance.date
        else:
            self.initial['date'] = date.today()

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        cleaned_data = super(WorkedHoursForm, self).clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        date = cleaned_data.get("date")

        intersect = WorkedHours.objects.filter(
            employee=self.employee,
            date=date,
            start_time__lte=end_time,
            end_time__gte=start_time
        )

        if self.instance.id:
            intersect = intersect.exclude(pk=self.instance.pk)

        if intersect.exists() > 0:
            self.add_error(
                'date',
                'Godziny w danym dniu się nakładają.'
            )

        if start_time > end_time:
            self.add_error(
                'start_time',
                'Czas rozpoczęcia jest później niż czas zakończenia.'
            )
