from django import forms

from .models import WorkedHours

class WorkedHoursForm(forms.ModelForm):
    """Responsible for setting up WorkedHours model."""
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = WorkedHours
        exclude = ['employee']
        fields = (
            'start_time',
            'end_time',
            'date'
        )


    def __init__(self, *args, **kwargs):
        """Initialize all Worked Hours's fields."""

        kwargs.setdefault('label_suffix', '')

        super(WorkedHoursForm, self).__init__(*args, **kwargs)

        self.fields['start_time'].label = 'Godzina rozpoczęcia'
        self.fields['end_time'].label = 'Godzina zakończenia'
        self.fields['date'].label = 'Dzień'

        if self.instance:
            self.initial['start_time'] = self.instance.start_time
            self.initial['end_time'] = self.instance.end_time
            self.initial['date'] = self.instance.date