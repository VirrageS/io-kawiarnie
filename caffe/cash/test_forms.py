# -*- encoding: utf-8 -*-

from django.test import TestCase

from caffe.models import Caffe
from employees.models import Employee

from .forms import CashReportForm, CompanyForm, ExpenseForm, FullExpenseForm
from .models import Company, Expense


class CompanyFormTest(TestCase):
    """Tests Company form."""

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

    def test_company(self):
        """Check validation."""

        bad_company = CompanyForm(
            {'name': ''},
            caffe=self.caffe
        )

        self.assertFalse(bad_company.is_valid())

        good_company = CompanyForm(
            {'name': 'very good'},
            caffe=self.caffe
        )

        self.assertTrue(good_company.is_valid())
        good_company.save()

        copycat_company = CompanyForm(
            {'name': 'very good'},
            caffe=self.caffe
        )
        self.assertFalse(copycat_company.is_valid())

        with self.assertRaises(Exception):
            CompanyForm({'bakery'})

    def test_name_validation(self):
        """Check name validation."""

        # same name, different caffes
        Company.objects.create(name='Bakery', caffe=self.filtry)

        form_correct = CompanyForm(
            {'name': 'Bakery'},
            caffe=self.caffe
        )
        self.assertTrue(form_correct.is_valid())

        # same name, same caffes
        Company.objects.create(name='Bakery', caffe=self.caffe)

        form_incorrect = CompanyForm(
            {'name': 'Bakery'},
            caffe=self.caffe
        )
        self.assertFalse(form_incorrect.is_valid())


class ExpenseFormTest(TestCase):
    """Tests Expense form."""

    def setUp(self):
        """Prepare objects for tests."""

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

        self.company = Company.objects.create(
            name='GoodCake',
            caffe=self.caffe
        )

        self.company_f = Company.objects.create(
            name='GoodCake',
            caffe=self.filtry
        )

    def test_validation(self):
        """Check validation."""

        empty_name_expense = ExpenseForm(
            {'name': '', 'company': self.company},
            caffe=self.caffe
        )
        self.assertFalse(empty_name_expense.is_valid())

        empty_company_expense1 = ExpenseForm(
            {'name': 'newspapers'},
            caffe=self.caffe
        )
        self.assertTrue(empty_company_expense1.is_valid())

        empty_company_expense2 = ExpenseForm(
            {'name': 'newspapers', 'company': None},
            caffe=self.caffe
        )
        self.assertTrue(empty_company_expense2.is_valid())

        empty_company_expense3 = ExpenseForm(
            {'name': 'newspapers', 'company': ''},
            caffe=self.caffe
        )
        self.assertTrue(empty_company_expense3.is_valid())

        complete_expense = ExpenseForm(
            {'name': 'cakes', 'company': self.company.pk},
            caffe=self.caffe
        )
        self.assertTrue(complete_expense.is_valid())

        different_caffe = ExpenseForm(
            {'name': 'cakes', 'company': self.company.pk},
            caffe=self.filtry
        )
        with self.assertRaises(Exception):
            different_caffe.save()

        with self.assertRaises(Exception):
            ExpenseForm({'name': 'cakes', 'company': self.company.pk})

    def test_name_validation(self):
        """Check name validation."""

        Expense.objects.create(
            name='cakes',
            company=self.company_f,
            caffe=self.filtry
        )

        form_correct = ExpenseForm(
            {'name': 'cakes', 'company': self.company.pk},
            caffe=self.caffe
        )
        self.assertTrue(form_correct.is_valid())

        # invalid name
        Expense.objects.create(
            name='cakes',
            company=self.company,
            caffe=self.caffe
        )

        form_incorrect = ExpenseForm(
            {'name': 'cakes', 'company': self.company.pk},
            caffe=self.caffe
        )
        self.assertFalse(form_incorrect.is_valid())


class FullExpenseFormTest(TestCase):
    """Tests FullExpense form."""

    def setUp(self):
        """Prepare objects for tests."""

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

        self.company = Company.objects.create(
            name='GoodCake',
            caffe=self.caffe
        )

        self.expense = Expense.objects.create(
            name='cakes',
            company=self.company,
            caffe=self.caffe
        )

    def test_validation(self):
        """Test validation."""

        cakes_for_10 = FullExpenseForm(
            {'expense': self.expense.pk, 'amount': 10},
            caffe=self.caffe
        )
        self.assertTrue(cakes_for_10.is_valid())

        cakes_for_nothing = FullExpenseForm(
            {'expense': self.expense.pk, 'amount': None},
            caffe=self.caffe
        )
        self.assertFalse(cakes_for_nothing.is_valid())

        money_for_nothing = FullExpenseForm(
            {'expense': None, 'amount': 10},
            caffe=self.caffe
        )
        self.assertFalse(money_for_nothing.is_valid())

        different_caffe = FullExpenseForm(
            {'expense': self.expense.pk, 'amount': 1},
            caffe=self.filtry
        )
        self.assertFalse(different_caffe.is_valid())


class CashReportFormTest(TestCase):
    """Tests CashReport form."""

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

        self.kate = Employee.objects.create(
            username='KateT',
            first_name='Kate',
            last_name='Tempest',
            telephone_number='12345678',
            email='kate@tempest.com',
            favorite_coffee='flat white',
            caffe=self.caffe
        )

    def test_validation(self):
        """Test validation of CashReport form."""

        no_cash_report = CashReportForm(
            {'card_payments': 500, 'amount_due': 1700},
            creator=self.kate,
            caffe=self.caffe,
        )
        self.assertFalse(no_cash_report.is_valid())

        no_cards_report = CashReportForm(
            {
                'cash_before_shift': 1000,
                'cash_after_shift': 2000,
                'amount_due': 1700
            },
            creator=self.kate,
            caffe=self.caffe
        )
        self.assertFalse(no_cards_report.is_valid())

        no_due_report = CashReportForm(
            {
                'card_payments': 500,
                'cash_before_shift': 1000,
                'cash_after_shift': 2000,
            },
            creator=self.kate,
            caffe=self.caffe
        )
        self.assertFalse(no_due_report.is_valid())

        perfectly_fine_report = CashReportForm(
            {
                'card_payments': 500,
                'cash_before_shift': 1000,
                'cash_after_shift': 2000,
                'amount_due': 1700
            },
            creator=self.kate,
            caffe=self.caffe
        )
        self.assertTrue(perfectly_fine_report.is_valid())

        different_caffe = CashReportForm(
            {
                'card_payments': 500,
                'cash_before_shift': 1000,
                'cash_after_shift': 2000,
                'amount_due': 1700
            },
            creator=self.kate,
            caffe=self.filtry
        )
        with self.assertRaises(Exception):
            different_caffe.save()

        with self.assertRaises(Exception):
            CashReportForm(
                {
                    'card_payments': 500,
                    'cash_before_shift': 1000,
                    'cash_after_shift': 2000,
                    'amount_due': 1700
                },
                creator=self.kate
            )

        with self.assertRaises(Exception):
            CashReportForm(
                {
                    'card_payments': 500,
                    'cash_before_shift': 1000,
                    'cash_after_shift': 2000,
                    'amount_due': 1700
                },
                caffe=self.caffe
            )
