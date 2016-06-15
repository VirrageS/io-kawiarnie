"""Module responsible for collecting cash reports data from users."""

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import CashReport, Company, Expense, FullExpense


class CompanyForm(forms.ModelForm):
    """Responsible for creating a Company."""

    class Meta:
        model = Company
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Company's fields."""

        self._caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'

    def clean_name(self):
        """Check name field."""

        name = self.cleaned_data['name']
        query = Company.objects.filter(name=name, caffe=self._caffe)
        if query.exists():
            raise ValidationError(_('Nazwa nie jest unikalna.'))

        return name

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        company = super(CompanyForm, self).save(commit=False)
        company.caffe = self._caffe
        if commit:
            company.save()

        return company


class ExpenseForm(forms.ModelForm):
    """Responsible for creating an object a cafe pays for during the day."""

    class Meta:
        model = Expense
        fields = ('name', 'company',)

    def __init__(self, *args, **kwargs):
        """Initialize all Expense's fields."""

        self._caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['company'].label = 'Firma'
        self.fields['company'].required = False

    def clean_name(self):
        """Check name field."""

        name = self.cleaned_data['name']
        query = Expense.objects.filter(name=name, caffe=self._caffe)
        if query.exists():
            raise ValidationError(_('Nazwa nie jest unikalna.'))

        return name

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        expense = super(ExpenseForm, self).save(commit=False)
        expense.caffe = self._caffe
        if commit:
            expense.save()

        return expense


class FullExpenseForm(forms.ModelForm):
    """Responsible for creating a full expense - expense and sum."""

    class Meta:
        model = FullExpense
        fields = ('expense', 'amount',)

    def __init__(self, *args, **kwargs):
        """Initialize all FullExpense's fields."""

        self._caffe = kwargs.pop('caffe')

        kwargs.setdefault('label_suffix', '')
        super(FullExpenseForm, self).__init__(*args, **kwargs)
        self.fields['expense'].label = 'Przeznaczenie'
        self.fields['amount'].label = 'Kwota'
        self.fields['expense'].empty_label = None

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        full_expense = super(FullExpenseForm, self).save(commit=False)
        full_expense._caffe = self._caffe
        if commit:
            full_expense.save()

        return full_expense


class CashReportForm(forms.ModelForm):
    """Responsible for creating a cash report."""

    class Meta:
        model = CashReport
        fields = [
            'cash_before_shift',
            'cash_after_shift',
            'card_payments',
            'amount_due'
        ]

    def __init__(self, *args, **kwargs):
        """Initialize all CashReport's fields."""

        self._caffe = kwargs.pop('caffe')
        self._creator = kwargs.pop('creator')

        kwargs.setdefault('label_suffix', '')
        super(CashReportForm, self).__init__(*args, **kwargs)
        self.fields['cash_before_shift'].label = 'Pieniądze na początku zmiany'
        self.fields['cash_after_shift'].label = 'Pieniądze na końcu zmiany'
        self.fields['card_payments'].label = 'Karty'
        self.fields['amount_due'].label = 'Łączna należność'

    def save(self, commit=True):
        """Override of save method, to add Caffe relation."""

        cash_report = super(CashReportForm, self).save(commit=False)
        cash_report.caffe = self._caffe
        cash_report.creator = self._creator
        if commit:
            cash_report.save()

        return cash_report
