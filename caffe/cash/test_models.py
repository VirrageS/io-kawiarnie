"""Cash reports models testing module."""

from django.test import TestCase

from employees.models import Employee

from .models import CashReport, Company, Expense, FullExpense


class CashReportModelTest(TestCase):
    """Cash report model tests."""

    def setUp(self):
        """Prepare data for tests."""

        self.Kate = Employee.objects.create(
            username='KateT',
            first_name='Kate',
            last_name='Tempest',
            telephone_number='12345678',
            email='kate@tempest.com',
            favorite_coffee='flat white'
        )

        self.report = CashReport.objects.create(
            author=self.Kate,
            cash_before_shift=2000,
            cash_after_shift=3000,
            card_payments=500,
            amount_due=1900,

        )

        self.GoodCake = Company.objects.create(name='GoodCake')
        self.Tesco = Company.objects.create(name='Tesco')

        self.cakes = Expense.objects.create(name='Cakes', company=self.GoodCake)
        self.supply = Expense.objects.create(name='Supply', company=self.Tesco)

        self.cake_expense = FullExpense.objects.create(
            destination=self.cakes,
            sum=50,
            report=self.report
        )

        self.supply_expense = FullExpense.objects.create(
            destination=self.supply,
            sum=500,
            report=self.report
        )

    def test_balance(self):
        self.assertEqual(self.report.balance(), 150)
