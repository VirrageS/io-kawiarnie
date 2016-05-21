"""Cash reports models testing module."""

from django.test import TestCase

from employees.models import Employee

from .models import CashReport, Company, Expense, FullExpense


class CashReportModelTest(TestCase):
    """Cash report model tests."""

    def setUp(self):
        """Prepare data for tests."""

        Employee.objects.create(
            username='KateT',
            first_name='Kate',
            last_name='Tempest',
            telephone_number='12345678',
            email='kate@tempest.com',
            favorite_coffee='flat white'
        )

        CashReport.objects.create(
            author=Employee.objects.get(username='KateT'),
            cash_before_shift=2000,
            cash_after_shift=3000,
            card_payments=500,
            amount_due=1900,

        )

        Company.objects.create(name='GoodCake')
        Company.objects.create(name='Tesco')

        Expense.objects.create(
            name='Cakes',
            company=Company.objects.get(name='GoodCake')
        )

        Expense.objects.create(
            name='Supply',
            company=Company.objects.get(name='Tesco')
        )

        FullExpense.objects.create(
            destination=Expense.objects.get(name='Cakes'),
            sum=50,
            report=CashReport.objects.first()
        )

        FullExpense.objects.create(
            destination=Expense.objects.get(name='Supply'),
            sum=500,
            report=CashReport.objects.first()
        )

    def test_balance(self):
        """Check if balance function works properly."""

        self.assertEqual(CashReport.objects.first().balance(), 150)
