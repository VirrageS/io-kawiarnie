# -*- encoding: utf-8 -*-

from django.contrib.auth.models import Permission
from django.core.urlresolvers import NoReverseMatch, reverse
from django.test import Client, TestCase

from caffe.models import Caffe

from .forms import EmployeeForm
from .models import Employee


class EmployeeViewsTests(TestCase):
    """Test all views of the Employee model."""

    def setUp(self):
        """Initiate everything needed in tests."""

        self.client = Client()

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

        self.emp1 = Employee.objects.create_user(
            username='marta',
            password='pass',
            email='marta@marta.pl',
            telephone_number=324092342,
            favorite_coffee='kawa',
            caffe=self.caffe
        )
        self.emp1.user_permissions.add(
            Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='view_cashreport'),
            Permission.objects.get(codename='view_workedhours'),
        )
        self.emp2 = Employee.objects.create_user(
            username='szkarta',
            password='pass',
            email='szkarta@szkarta.pl',
            telephone_number=324092342,
            favorite_coffee='kawa',
            caffe=self.caffe
        )
        self.emp3 = Employee.objects.create_user(
            username='szkarta1',
            password='pass',
            email='szkarta@szkarta.pl',
            telephone_number=324092342,
            favorite_coffee='kawa',
            caffe=self.filtry
        )

        self.emp1.save()
        self.emp2.save()
        self.emp3.save()

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin',
            caffe=self.caffe
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_employee'),
            Permission.objects.get(codename='change_employee'),
            Permission.objects.get(codename='delete_employee'),
            Permission.objects.get(codename='view_employee'),

            Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='view_cashreport'),
            Permission.objects.get(codename='view_workedhours'),
        )

        self.client.login(username='admin', password='admin')

    def test_show_all_employees(self):
        """Check if employees are all displayed properly."""

        response = self.client.get(reverse('employees:all'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/all.html')

        self.assertEqual(len(response.context['employees']), 3)
        self.assertIn(self.emp1, response.context['employees'])
        self.assertIn(self.emp2, response.context['employees'])

    def test_navigate_employees(self):
        """Check if navigate view is displayed properly."""

        response = self.client.get(reverse('employees:navigate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/employees.html')

    def test_edit_employees_show(self):
        """Check if new employee view is displayed properly."""

        response = self.client.get(
            reverse('employees:edit', args=(self.emp1.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/edit.html')
        self.assertIsInstance(response.context['form'], EmployeeForm)
        self.assertEqual(response.context['employee'], self.emp1)

    def test_edit_employees_success(self):
        """Check if editing employees works as intended."""

        response = self.client.post(
            reverse('employees:edit', args=(self.emp1.id,)),
            {
                'username': 'kolega',
                'password1': 'qweweweuroiwieur',
                'password2': 'qweweweuroiwieur',
                'email': self.emp1.email,
                'telephone_number': self.emp1.telephone_number,
                'favorite_coffee': self.emp1.favorite_coffee
            },
            follow=True
        )

        self.assertRedirects(response, reverse('employees:navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        # check if employee has changed
        employee = Employee.objects.get(id=self.emp1.id)
        self.assertEqual(employee.username, u'kolega')
        self.assertEqual(employee.caffe, self.caffe)

        # check if edited employee is displayed
        response = self.client.get(reverse('employees:all'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['employees']), 3)

    def test_edit_employees_fail(self):
        """Check if editing fails on wrong data."""

        response = self.client.post(
            reverse('employees:edit', args=(self.emp1.id,)),
            {
                'username': '',
                'password1': 'qweweweuroiwieur',
                'password2': 'qweweweuroiwieur',
                'email': self.emp1.email,
                'telephone_number': self.emp1.telephone_number,
                'favorite_coffee': self.emp1.favorite_coffee
            },
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("niepoprawnie" in messages[0].message)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'username': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'employees/edit.html')

    def test_edit_employees_404(self):
        """Check if 404 is displayed when employee does not exists."""

        ids_for_404 = [self.emp3.id, 13, 23423, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('employees:edit', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('employees:edit', args=(_id,))

    def test_new_employees_show(self):
        """Check if creating employees works as intended."""

        response = self.client.get(reverse('employees:new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/new.html')
        self.assertIsInstance(response.context['form'], EmployeeForm)

    def test_new_employees_success(self):
        """Check if creating employees works as intended."""

        response = self.client.post(
            reverse('employees:new'),
            {
                'username': 'prac',
                'password1': 'qweweweuroiwieur',
                'password2': 'qweweweuroiwieur',

                'first_name': 'Prac',
                'last_name': 'Prac',
                'telephone_number': 545334534,
                'email': 'prac@prac.com',
                'favorite_coffee': 'Zbożowa'
            },
            follow=True
        )

        self.assertRedirects(response, reverse('employees:navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        # check if new employee is displayed
        response = self.client.get(reverse('employees:all'))
        self.assertEqual(response.status_code, 200)

        employees = list(response.context['employees'])
        self.assertEqual(len(employees), 4)
        self.assertListEqual(
            employees,
            sorted(
                employees,
                key=lambda employee: employee.last_name,
                reverse=False
            )
        )

        new_employee = Employee.objects.get(username='prac')
        self.assertIsNotNone(new_employee)
        self.assertIsInstance(new_employee, Employee)
        self.assertEqual(new_employee.caffe, self.user.caffe)
        self.assertEqual(new_employee.caffe, self.caffe)

    def test_new_employees_fail(self):
        """Check if creating employees fails correctly."""

        response = self.client.post(
            reverse('employees:new'),
            {
                'username': '',
                'password1': 'qweweweuroiwieur',
                'password2': 'qweweweuroiwieur',

                'first_name': 'Prac',
                'last_name': 'Prac',
                'telephone_number': 545334534,
                'email': 'prac@prac.com',
                'favorite_coffee': 'Zbożowa'
            },
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("niepoprawnie" in messages[0].message)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'username': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'employees/new.html')

    def test_login_employee_success(self):
        """Check if employee can login."""

        logged_in = self.client.login(username='marta', password='pass')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('employees:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/login.html')

        response = self.client.post(
            reverse('employees:login'),
            {
                'username': 'marta',
                'password': 'pass'
            },
            follow=True
        )

        self.assertRedirects(response, reverse('home:navigate'))

    def test_delete_employee_success(self):
        """Check if deleting employees works as intended."""

        response = self.client.post(
            reverse('employees:delete', args=(self.emp1.id,)),
            follow=True
        )

        self.assertRedirects(response, reverse('employees:navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        # try to get deleted employee
        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(id=self.emp1.id)

    def test_delete_employee_fail(self):
        """Check if deleting employees fails when trying to delete themself."""

        response = self.client.post(
            reverse('employees:delete', args=(self.user.id,)),
            follow=True
        )

        self.assertRedirects(response, reverse('employees:navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")

        # try to get deleted employee
        employee = Employee.objects.get(id=self.user.id)
        self.assertIsNotNone(employee)

    def test_delete_employee_404(self):
        """Check if 404 is displayed when employee does not exists."""

        ids_for_404 = [self.emp3.id, 13, 23423, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('employees:delete', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('employees:delete', args=(_id,))

    def test_login_employee_fail(self):
        """Check if employee login can fail."""

        logged_in = self.client.login(username='marta', password='passs')
        self.assertFalse(logged_in)

    def test_logout_employee_success(self):
        """Check if employee can logout."""

        logged_in = self.client.login(username='marta', password='pass')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('employees:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/logout.html')

    def test_logout_employee_fail(self):
        """Check if employee logout can fail."""

        # logout global user
        self.client.get(reverse('employees:logout'), follow=True)

        logged_in = self.client.login(username='marta', password='passs')
        self.assertFalse(logged_in)

        response = self.client.get(reverse('employees:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/login.html')
