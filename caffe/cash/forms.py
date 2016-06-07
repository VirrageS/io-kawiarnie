"""Module responsible for collecting cash reports data from users."""

from django import forms

from .models import CashReport, Company, Expense, FullExpense


class CompanyForm(forms.ModelForm):
    """Responsible for creating a Company."""

    class Meta:
        model = Company
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """Initialize all Company's fields."""

        kwargs.setdefault('label_suffix', '')
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'


class ExpenseForm(forms.ModelForm):
    """Responsible for creating an object a cafe pays for during the day."""

    class Meta:
        model = Expense
        fields = ('name', 'company',)

    def __init__(self, *args, **kwargs):
        """Initialize all Expense's fields."""

        kwargs.setdefault('label_suffix', '')
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['company'].label = 'Firma'
        self.fields['company'].required = False


class FullExpenseForm(forms.ModelForm):
    """Responsible for creating a full expense - expense and sum."""

    class Meta:
        model = FullExpense
        fields = ('expense', 'amount',)

    def __init__(self, *args, **kwargs):
        """Initialize all FullExpense's fields."""

        kwargs.setdefault('label_suffix', '')
        super(FullExpenseForm, self).__init__(*args, **kwargs)
        self.fields['expense'].label = 'Przeznaczenie'
        self.fields['amount'].label = 'Kwota'
        self.fields['expense'].empty_label = None


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

        kwargs.setdefault('label_suffix', '')
        super(CashReportForm, self).__init__(*args, **kwargs)
        self.fields['cash_before_shift'].label = 'Pieniądze na początku zmiany'
        self.fields['cash_after_shift'].label = 'Pieniądze na końcu zmiany'
        self.fields['card_payments'].label = 'Karty'
        self.fields['amount_due'].label = 'Łączna należność'
