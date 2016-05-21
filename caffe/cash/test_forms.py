"""Cash reports forms test module."""

from django.test import TestCase

from .forms import CompanyForm, ExpenseForm, FullExpenseForm
from .models import Company, Expense, FullExpense


class CompanyFormTest(TestCase):
    """Tests Company form."""

    def test_validation(self):
        """Checks validation."""

        bad_company = CompanyForm({
            'name': ''
        })

        self.assertFalse(bad_company.is_valid())

        good_company = CompanyForm({
            'name': 'very good'
        })

        good_company.save()

        self.assertTrue(good_company.is_valid())

        copycat_company = CompanyForm({
            'name': 'very good'
        })

        self.assertFalse(copycat_company.is_valid())


class ExpenseFormTest(TestCase):
    """Tests Expense form."""

    def setUp(self):
        """Prepares objects for tests."""
        self.company = Company.objects.create(name='GoodCake')

    def test_validation(self):
        """Checks validation."""

        empty_name_expense = ExpenseForm({
            'name': '',
            'company': self.company
        })

        self.assertFalse(empty_name_expense.is_valid())

        empty_company_expense1 = ExpenseForm({
            'name': 'newspapers'
        })

        self.assertTrue(empty_company_expense1.is_valid())

        empty_company_expense2 = ExpenseForm({
            'name': 'newspapers',
            'company': None
        })

        self.assertTrue(empty_company_expense2.is_valid())

        empty_company_expense3 = ExpenseForm({
            'name': 'newspapers',
            'company': ''
        })

        self.assertTrue(empty_company_expense3.is_valid())

        complete_expense = ExpenseForm({
            'name': 'cakes',
            'company': self.company.pk
        })

        self.assertTrue(complete_expense.is_valid())


class FullExpenseFormTest(TestCase):
    """Tests FullExpense form."""

    def setUp(self):
        """Prepares objects for tests."""

        self.company = Company.objects.create(name='GoodCake')
        self.expense = Expense.objects.create(
            name='cakes',
            company=self.company
        )

    def test_validation(self):
        """Tests validation."""

        cakes_for_10 = FullExpenseForm({
            'destination': self.expense.pk,
            'sum': 10
        })

        self.assertTrue(cakes_for_10.is_valid())

        cakes_for_nothing = FullExpenseForm({
            'destination': self.expense.pk,
            'sum': None
        })

        self.assertFalse(cakes_for_nothing.is_valid())

        money_for_nothing = FullExpenseForm({
            'destination': None,
            'sum': 10
        })

        self.assertFalse(money_for_nothing.is_valid())
