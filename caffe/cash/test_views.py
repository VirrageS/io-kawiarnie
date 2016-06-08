"""Testing module for Cash views."""
# -*- encoding: utf-8 -*-
# pylint: disable=C0103,R0902


from django.contrib.auth.models import Permission
from django.core.urlresolvers import NoReverseMatch, reverse
from django.test import Client, TestCase

from employees.models import Employee

from .forms import CashReportForm, CompanyForm, ExpenseForm
from .models import CashReport, Company, Expense, FullExpense


class CompanyViewsTests(TestCase):
    """Test all views of the Company model."""

    def setUp(self):
        """Initialize all Company needed in tests."""

        self.client = Client()

        self.putka = Company.objects.create(name='Putka')
        self.kolporter = Company.objects.create(name='Kolporter')

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_company'),
            Permission.objects.get(codename='change_company'),
            Permission.objects.get(codename='view_company'),
        )

        self.client.login(username='admin', password='admin')

    def test_new_company_show(self):
        """Check if new company view is displayed properly."""

        response = self.client.get(reverse('cash_new_company'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], CompanyForm)
        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            'Nowa firma'
        )

        elements = response.context['elements']
        self.assertEqual(len(elements), 2)
        self.assertListEqual(
            elements,
            sorted(elements, key=lambda x: x['desc'], reverse=False)
        )

        for element in elements:
            self.assertEqual(len(element), 3)
            self.assertIn(
                element['edit_href'], [
                    reverse('cash_edit_company', args=(self.putka.id,)),
                    reverse('cash_edit_company', args=(self.kolporter.id,))
                ]
            )
            self.assertIn(element['id'], [self.putka.id, self.kolporter.id])
            self.assertIn(
                element['desc'],
                [str(self.putka), str(self.kolporter)]
            )

    def test_new_company_post_fail(self):
        """Check if new company fails to create when form is not valid."""

        response = self.client.post(
            reverse('cash_new_company'),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'cash/new_element.html')

    def test_new_company_post_success(self):
        """Check if new company successes to create when form is valid."""

        response = self.client.post(
            reverse('cash_new_company'),
            {u'name': u'Bambino'},
            follow=True
        )

        self.assertRedirects(response, reverse('cash_navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        # check if new company is displayed
        response = self.client.get(reverse('cash_new_company'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)
        self.assertListEqual(
            response.context['elements'],
            sorted(
                response.context['elements'],
                key=lambda x: x['desc'],
                reverse=False
            )
        )

        new_company = Company.objects.get(name='Bambino')
        self.assertIsNotNone(new_company)
        self.assertIsInstance(new_company, Company)

    def test_edit_company_show(self):
        """Check if edit company view is displayed properly."""

        response = self.client.get(
            reverse('cash_edit_company', args=(self.putka.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, CompanyForm)
        self.assertEqual(form.instance, self.putka)

        self.assertEqual(len(response.context['context']), 2)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj firmę'
        )
        self.assertEqual(
            response.context['context']['cancel_href'],
            reverse('cash_new_company')
        )

    def test_edit_company_404(self):
        """Check if 404 is displayed when company does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('cash_edit_expense', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('cash_edit_expense', args=(_id,))

    def test_edit_company_post_fail(self):
        """Check if edit company fails to edit when form is not valid."""

        response = self.client.post(
            reverse('cash_edit_company', args=(self.putka.id,)),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
        })

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        self.assertTemplateUsed(response, 'cash/edit_element.html')

    def test_edit_company_post_success(self):
        """Check if edit company successes to edit when form is valid."""

        response = self.client.post(
            reverse('cash_edit_company', args=(self.putka.id,)),
            {u'name': u'Bambino'},
            follow=True
        )

        self.assertRedirects(response, reverse('cash_navigate'))

        # check if company name has changed
        company = Company.objects.get(id=self.putka.id)
        self.assertEqual(company.name, u'Bambino')

        # check if edited company is displayed
        response = self.client.get(reverse('cash_new_company'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class ExpenseViewsTests(TestCase):
    """Test all views of the Expense model."""

    def setUp(self):
        """Initialize all expenses needed in tests."""

        self.client = Client()

        self.putka = Company.objects.create(name='Putka')
        self.kolporter = Company.objects.create(name='Kolporter')

        self.newspapers = Expense.objects.create(
            name='Newspapers'
        )

        self.cakes = Expense.objects.create(
            name='Ciasta',
            company=self.kolporter
        )

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_expense'),
            Permission.objects.get(codename='change_expense'),
            Permission.objects.get(codename='view_expense'),
        )

        self.client.login(username='admin', password='admin')

    def test_new_expense_show(self):
        """Check if new expense view is displayed properly."""

        response = self.client.get(reverse('cash_new_expense'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], ExpenseForm)
        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            'Nowy wydatek'
        )

        elements = response.context['elements']
        self.assertEqual(len(elements), 2)
        self.assertListEqual(
            elements,
            sorted(elements, key=lambda x: x['desc'], reverse=False)
        )

        for element in elements:
            self.assertEqual(len(element), 3)
            self.assertIn(
                element['edit_href'], [
                    reverse('cash_edit_expense', args=(self.newspapers.id,)),
                    reverse('cash_edit_expense', args=(self.cakes.id,))
                ]
            )
            self.assertIn(element['id'], [self.newspapers.id, self.cakes.id])
            self.assertIn(
                element['desc'],
                [str(self.newspapers), str(self.cakes)]
            )

    def test_new_expense_post_fail(self):
        """Check if new expense fails to create when form is not valid."""

        response = self.client.post(
            reverse('cash_new_expense'),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
        })

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        self.assertTemplateUsed(response, 'cash/new_element.html')

    def test_new_expense_post_success(self):
        """Check if new expense successes to create when form is valid."""

        response = self.client.post(
            reverse('cash_new_expense'),
            {'name': u'Magazyny', 'company': self.kolporter.id},
            follow=True
        )

        self.assertRedirects(response, reverse('cash_navigate'))

        # check if new expense is displayed
        response = self.client.get(reverse('cash_new_expense'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)
        self.assertListEqual(
            response.context['elements'],
            sorted(
                response.context['elements'],
                key=lambda x: x['desc'],
                reverse=False
            )
        )

        new_expense = Expense.objects.get(name='Magazyny')
        self.assertIsNotNone(new_expense)
        self.assertIsInstance(new_expense, Expense)

    def test_edit_expense_show(self):
        """Check if edit expense view is displayed properly."""

        response = self.client.get(
            reverse('cash_edit_expense', args=(self.newspapers.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, ExpenseForm)
        self.assertEqual(form.instance, self.newspapers)

        self.assertEqual(len(response.context['context']), 2)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj wydatek'
        )
        self.assertEqual(
            response.context['context']['cancel_href'],
            reverse('cash_new_expense')
        )

    def test_edit_expense_404(self):
        """Check if 404 is displayed when expense does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('cash_edit_expense', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('cash_edit_expense', args=(_id,))

    def test_edit_expense_post_fail(self):
        """Check if edit expense fails to edit when form is not valid."""

        response = self.client.post(
            reverse('cash_edit_expense', args=(self.newspapers.id,)),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
        })

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        self.assertTemplateUsed(response, 'cash/edit_element.html')

    def test_edit_expense_post_success(self):
        """Check if edit expense successes to edit when form is valid."""

        response = self.client.post(
            reverse('cash_edit_expense', args=(self.newspapers.id,)),
            {u'name': u'Magazines'},
            follow=True
        )

        self.assertRedirects(response, reverse('cash_navigate'))

        # check if expense name has changed
        expense = Expense.objects.get(id=self.newspapers.id)
        self.assertEqual(expense.name, u'Magazines')

        # check if edited expense is displayed
        response = self.client.get(reverse('cash_new_expense'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class CashReportViewTests(TestCase):
    """Tests views for CashReport model."""

    def setUp(self):
        """Initialize each test."""

        self.client = Client()

        self.putka = Company.objects.create(name='Putka')
        self.kolporter = Company.objects.create(name='Kolporter')

        self.newspapers = Expense.objects.create(
            name='Newspapers'
        )

        self.cakes = Expense.objects.create(
            name='Ciasta',
            company=self.kolporter
        )

        self.full_newspapers = FullExpense.objects.create(
            expense=self.newspapers,
            amount=100
        )

        self.full_cakes = FullExpense.objects.create(
            expense=self.cakes,
            amount=200
        )

        self.full_cakes_second = FullExpense.objects.create(
            expense=self.cakes,
            amount=400
        )

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_cashreport'),
            Permission.objects.get(codename='change_cashreport'),
            Permission.objects.get(codename='view_cashreport'),
        )

        self.client.login(username='admin', password='admin')

        self.cash_report_main = CashReport(
            cash_before_shift=1000,
            cash_after_shift=1200,
            card_payments=123,
            amount_due=100
        )
        self.cash_report_main.creator = self.user
        self.cash_report_main.save()

        self.cash_report_minor = CashReport(
            cash_before_shift=10,
            cash_after_shift=12,
            card_payments=11,
            amount_due=1
        )
        self.cash_report_minor.creator = self.user
        self.cash_report_minor.save()

        self.full_newspapers.cash_report = self.cash_report_main
        self.full_cakes.cash_report = self.cash_report_main
        self.full_newspapers.save()
        self.full_cakes.save()

        self.full_cakes_second.cash_report = self.cash_report_minor
        self.full_cakes_second.save()

    def test_cash_navigate(self):
        """Check if navigate view for CashReport is displayed properly."""

        response = self.client.get(reverse('cash_navigate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/cash.html')

    def test_cashreport_show_all(self):
        """Check if all CashReport view is displayed properly."""

        response = self.client.get(reverse('show_all_cash_reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/all.html')

        # check context
        self.assertEqual(len(response.context['reports']), 2)
        reports = list(response.context['reports'])
        self.assertListEqual(
            reports,
            sorted(reports, key=lambda cash: cash.created_on, reverse=True)
        )

    def test_cashreport_show(self):
        """Check if CashReport view is displated properly."""
        response = self.client.get(reverse(
            'show_cash_report',
            args=(self.cash_report_main.id,)
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/show.html')

        report = response.context['report']
        expenses = response.context['expenses']

        self.assertEqual(report, self.cash_report_main)
        self.assertEqual(len(expenses), 2)

    def test_edit_cashreport_show(self):
        """Check if edit CashReport view is displayed properly."""

        response = self.client.get(
            reverse('edit_cash_report', args=(self.cash_report_main.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/new_report.html')

        form = response.context['form']
        self.assertIsInstance(form, CashReportForm)
        self.assertEqual(form.instance, self.cash_report_main)

    def test_edit_cashreport_post_success(self):
        """Check success of edit CashReport post request."""

        post = {}
        post['cash_before_shift'] = 1
        post['cash_after_shift'] = 1
        post['card_payments'] = 1
        post['amount_due'] = 1
        post[self.newspapers.id] = [self.newspapers.id, 10000]

        response = self.client.post(
            reverse('edit_cash_report', args=(self.cash_report_main.id,)),
            post,
            follow=True
        )

        self.assertRedirects(response, reverse('cash_navigate'))
        self.assertEqual(CashReport.objects.count(), 2)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        report = CashReport.objects.get(id=self.cash_report_main.id)
        self.assertEqual(report.cash_before_shift, 1)
        self.assertEqual(report.cash_after_shift, 1)
        self.assertEqual(report.card_payments, 1)
        self.assertEqual(report.amount_due, 1)

        expenses = report.full_expense.all()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 10000)

    def test_edit_cashreport_post_failure(self):
        """Check failure of edit CashReport post request."""

        post = {}
        post['cash_before_shift'] = 1
        post['cash_after_shift'] = 1
        post['card_payments'] = 1
        post[self.newspapers.id] = [self.newspapers.id, 10000]

        response = self.client.post(
            reverse('edit_cash_report', args=(self.cash_report_main.id,)),
            post,
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("niepoprawnie" in messages[0].message)

        post = {}
        post['cash_before_shift'] = 1
        post['cash_after_shift'] = 1
        post['card_payments'] = 1
        post['amount_due'] = 1
        post[-self.newspapers.id] = [-self.newspapers.id, -10000]

        response = self.client.post(
            reverse('edit_cash_report', args=(self.cash_report_main.id,)),
            post,
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("niepoprawnie" in messages[0].message)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/new_report.html')

    def test_new_cashreport(self):
        """Check form to create new CashReport."""

        response = self.client.get(reverse('new_cash_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/new_report.html')

    def test_new_cashreport_post_success(self):
        """Check success of new CashReport post request."""

        post = {}
        post['cash_before_shift'] = 1
        post['cash_after_shift'] = 1
        post['card_payments'] = 1
        post['amount_due'] = 1
        post[self.newspapers.id] = [self.newspapers.id, 10000]

        response = self.client.post(
            reverse('new_cash_report'),
            post,
            follow=True
        )

        self.assertRedirects(response, reverse('cash_navigate'))
        self.assertEqual(CashReport.objects.count(), 3)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        report = CashReport.objects.latest('created_on')

        self.assertEqual(report.creator, self.user)
        self.assertEqual(report.cash_before_shift, 1)
        self.assertEqual(report.cash_after_shift, 1)
        self.assertEqual(report.card_payments, 1)
        self.assertEqual(report.amount_due, 1)

        expenses = report.full_expense.all()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 10000)

    def test_new_cashreport_post_failure(self):
        """Check failure of new CashReport post request."""

        post = {}
        post['cash_before_shift'] = 1
        post['cash_after_shift'] = 1
        post['card_payments'] = 1
        post[self.newspapers.id] = [self.newspapers.id, 10000]

        response = self.client.post(
            reverse('new_cash_report'),
            post,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/new_report.html')
        self.assertEqual(CashReport.objects.count(), 2)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("niepoprawnie" in messages[0].message)

        post = {}
        post['cash_before_shift'] = 1
        post['cash_after_shift'] = 1
        post['card_payments'] = 1
        post['amount_due'] = 1
        post[-self.newspapers.id] = [-self.newspapers.id, 10000]

        response = self.client.post(
            reverse('new_cash_report'),
            post,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash/new_report.html')
        self.assertEqual(CashReport.objects.count(), 2)
