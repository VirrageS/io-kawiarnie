"""Cash reports models testing module."""

from django.test import TestCase

from caffe.models import Caffe
from employees.models import Employee

from .models import CashReport, Company, Expense, FullExpense


class CashReportModelTest(TestCase):
    """Cash report model tests."""

    def setUp(self):
        """Prepare data for tests."""

        self.caffe = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )
        self.filtry = Caffe.objects.create(
            name='filtry',
            city='Warszawa',
            street='Filry',
            house_number='14',
            postal_code='44-100'
        )

        self.kate = Employee.objects.create(
            username='KateT',
            first_name='Kate',
            last_name='Tempest',
            telephone_number='12345678',
            email='kate@tempest.com',
            favorite_coffee='flat white',
            caffe=self.caffe
        )

        self.cash_report = CashReport.objects.create(
            creator=self.kate,
            caffe=self.caffe,
            cash_before_shift=2000,
            cash_after_shift=3000,
            card_payments=500,
            amount_due=1900
        )

        Company.objects.create(name='GoodCake', caffe=self.caffe)
        Company.objects.create(name='Tesco', caffe=self.caffe)

        Expense.objects.create(
            name='Cakes',
            company=Company.objects.get(name='GoodCake'),
            caffe=self.caffe
        )

        Expense.objects.create(
            name='Supply',
            company=Company.objects.get(name='Tesco'),
            caffe=self.caffe
        )

        FullExpense.objects.create(
            expense=Expense.objects.get(name='Cakes'),
            amount=50,
            cash_report=CashReport.objects.first(),
            caffe=self.caffe
        )

        FullExpense.objects.create(
            expense=Expense.objects.get(name='Supply'),
            amount=500,
            cash_report=CashReport.objects.first(),
            caffe=self.caffe
        )

    def test_balance(self):
        """Check if balance function works properly."""

        self.assertEqual(self.cash_report.balance(), 150)

    def test_cash_report_validation(self):
        """Check cash report validation."""

        self.assertEqual(self.cash_report.caffe, self.caffe)

        with self.assertRaises(Exception):
            CashReport.objects.create(
                creator=self.kate,
                caffe=self.filtry,
                cash_before_shift=2000,
                cash_after_shift=3000,
                card_payments=500,
                amount_due=1900
            )


class CompanyModelTest(TestCase):
    """Company model tests."""

    def setUp(self):
        """Test data setup."""

        self.caffe = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )
        self.filtry = Caffe.objects.create(
            name='filtry',
            city='Warszawa',
            street='Filry',
            house_number='14',
            postal_code='44-100'
        )

        self.bakery = Company.objects.create(name="bakery", caffe=self.caffe)
        Company.objects.create(name="newspapers company", caffe=self.caffe)

    def test_name(self):
        """Check if name is unique across one caffe."""

        self.assertEqual(self.bakery.name, "bakery")
        self.assertEqual(self.bakery.caffe, self.caffe)

        with self.assertRaises(Exception):
            Company.objects.create(name="bakery", caffe=self.caffe)

        Company.objects.create(name="bakery", caffe=self.filtry)


class ExpenseModelTest(TestCase):
    """Expense model tests."""

    def setUp(self):
        """Test data setup."""

        self.caffe = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )
        self.filtry = Caffe.objects.create(
            name='filtry',
            city='Warszawa',
            street='Filry',
            house_number='14',
            postal_code='44-100'
        )

        self.bakery = Company.objects.create(name="bakery", caffe=self.caffe)
        self.bakery_f = Company.objects.create(
            name="bakery",
            caffe=self.filtry
        )

        self.cakes = Expense.objects.create(
            name="cakes",
            company=self.bakery,
            caffe=self.caffe
        )

    def test_name(self):
        """Check if name is unique across one caffe."""

        self.assertEqual(self.bakery.name, "bakery")
        self.assertEqual(self.bakery.caffe, self.caffe)

        with self.assertRaises(Exception):
            Expense.objects.create(
                name="cakes",
                company=self.bakery,
                caffe=self.caffe
            )

        Expense.objects.create(
            name="cakes",
            company=self.bakery_f,
            caffe=self.filtry
        )

    def test_expense_validation(self):
        """Check expense validation."""

        with self.assertRaises(Exception):
            Expense.objects.create(
                name="cakes",
                company=self.bakery_f,
                caffe=self.caffe
            )

        with self.assertRaises(Exception):
            Expense.objects.create(
                name="cakes",
                company=self.bakery,
                caffe=self.filtry
            )


class FullExpenseModelTest(TestCase):
    """FullExpense model tests."""

    def setUp(self):
        """Test data setup."""

        self.kafo = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )
        self.filtry = Caffe.objects.create(
            name='filtry',
            city='Warszawa',
            street='Filry',
            house_number='14',
            postal_code='44-100'
        )

        self.bakery = Company.objects.create(name="bakery", caffe=self.kafo)
        self.bakery_f = Company.objects.create(
            name="bakery",
            caffe=self.filtry
        )

        self.cakes = Expense.objects.create(
            name="cakes",
            company=self.bakery,
            caffe=self.kafo
        )
        self.cakes_f = Expense.objects.create(
            name="cakes",
            company=self.bakery_f,
            caffe=self.filtry
        )

        self.full_cakes = FullExpense.objects.create(
            expense=self.cakes,
            amount=1,
            caffe=self.kafo
        )

        self.kate = Employee.objects.create(
            username='KateT',
            first_name='Kate',
            last_name='Tempest',
            telephone_number='12345678',
            email='kate@tempest.com',
            favorite_coffee='flat white',
            caffe=self.kafo
        )
        self.cash_report = CashReport.objects.create(
            creator=self.kate,
            caffe=self.kafo,
            cash_before_shift=2000,
            cash_after_shift=3000,
            card_payments=500,
            amount_due=1900
        )

    def test_full_expense_validation(self):
        """Check if name is unique across one caffe."""

        self.assertEqual(self.full_cakes.amount, 1)
        self.assertEqual(self.full_cakes.caffe, self.kafo)

        with self.assertRaises(Exception):
            FullExpense.objects.create(
                expense=self.cakes,
                amount=1,
                caffe=self.filtry
            )

        with self.assertRaises(Exception):
            FullExpense.objects.create(
                expense=self.cakes_f,
                amount=1,
                caffe=self.kafo
            )

        with self.assertRaises(Exception):
            FullExpense.objects.create(
                expense=self.cakes_f,
                amount=1,
                caffe=self.filtry,
                cash_report=self.cash_report
            )
