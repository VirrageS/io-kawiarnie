from django import forms

from .models import WorkedHours

class WorkedHoursForm(forms.ModelForm):
    """Responsible for setting up WorkedHours model."""

    class Meta:
        model = WorkedHours
        fields = (
            'employee',
            'start_time',
            'end_time',
            'date'
        )


    def __init__(self, *args, **kwargs):
        """Initialize all Product's fields."""

        kwargs.setdefault('label_suffix', '')
        super(WorkedHoursForm, self).__init__(*args, **kwargs)
        self.fields['employee'].label = 'Pracownik'
        self.fields['start_time'].label = 'Godzina rozpoczęcia'
        self.fields['end_time'].label = 'Godzina zakończenia'
        self.fields['date'].label = 'Dzień'