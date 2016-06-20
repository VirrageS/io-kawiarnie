from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from employees.forms import EmployeeForm
from employees.models import Employee

from .forms import CaffeForm
from .models import Caffe


class CaffeViewsTests(TestCase):
    """Test all views of the landing page."""

    def setUp(self):
        """Initialize all Caffe needed in tests."""

        self.client = Client()

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='view_cashreport'),
            Permission.objects.get(codename='view_workedhours'),
        )

        Group.objects.create(name='Admin')

    def test_landing_logged_out(self):
        """Check if landing page appears if user is not logged in."""

        response = self.client.get(reverse('index_navigate'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/landing_page.html')

    def test_landing_logged_in(self):
        """Check if landing page redirect if user is logged in."""

        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('index_navigate'), follow=True)
        self.assertRedirects(response, reverse('home:navigate'))

    def test_new_caffe_show(self):
        """Check if creating caffe shows good page."""

        response = self.client.get(reverse('caffe_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'caffe/new.html')
        self.assertIsInstance(response.context['caffe_form'], CaffeForm)
        self.assertIsInstance(response.context['admin_form'], EmployeeForm)

    def test_new_caffe_success(self):
        """Check if creating employees works as intended."""

        form = {
            'name': 'Caffe',
            'city': 'SanCaffe2',
            'street': 'CaffeStreet2',
            'postal_code': '00-100',
            'building_number': '50a',
            'house_number': '40',

            'username': 'prac',
            'password1': 'qweweweuroiwieur',
            'password2': 'qweweweuroiwieur',

            'first_name': 'Prac',
            'last_name': 'Prac',
            'email': 'prac@prac.com',
            'favorite_coffee': 'Zbożowa'
        }

        response = self.client.post(
            reverse('caffe_create'),
            form,
            follow=True
        )

        self.assertRedirects(response, reverse('employees:login'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        caffes = Caffe.objects.all()
        caffe = caffes[0]
        self.assertEqual(len(caffes), 1)
        self.assertEqual(caffe.name, 'Caffe')

        employees = Employee.objects.filter(caffe=caffe).all()
        employee = employees[0]
        self.assertEqual(len(employees), 1)
        self.assertEqual(employee.username, 'prac')
        self.assertEqual(employee.first_name, 'Prac')
        self.assertEqual(employee.last_name, 'Prac')
        self.assertIn(Group.objects.get(name='Admin'), employee.groups.all())

    def test_new_caffe_fails_caffe(self):
        """Check if creating employees works as intended."""

        form = {
            'name': '',
            'city': 'SanCaffe2',
            'street': 'CaffeStreet2',
            'postal_code': '00-100',
            'building_number': '50a',

            'username': 'prac',
            'password1': 'qweweweuroiwieur',
            'password2': 'qweweweuroiwieur',

            'first_name': 'Prac',
            'last_name': 'Prac',
            'telephone_number': 545334534,
            'email': 'prac@prac.com'
        }

        response = self.client.post(
            reverse('caffe_create'),
            form,
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("niepoprawnie" in messages[0].message)

        caffes = Caffe.objects.all()
        self.assertEqual(len(caffes), 0)

        employees = Employee.objects.all()
        self.assertEqual(len(employees), 1)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['caffe_form'].is_valid())
        self.assertEqual(response.context['caffe_form'].errors, {
            'name': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'caffe/new.html')

    def test_new_caffe_fails_admin(self):
        """Check if creating employees works as intended."""

        form = {
            'name': 'Caffe',
            'city': 'SanCaffe2',
            'street': 'CaffeStreet2',
            'postal_code': '00-100',
            'building_number': '50a',

            'username': '',
            'password1': 'qweweweuroiwieur',
            'password2': 'qweweweuroiwieur',

            'first_name': 'Prac',
            'last_name': 'Prac',
            'telephone_number': 545334534,
            'email': 'prac@prac.com'
        }

        response = self.client.post(
            reverse('caffe_create'),
            form,
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("niepoprawnie" in messages[0].message)

        caffes = Caffe.objects.all()
        self.assertEqual(len(caffes), 0)

        employees = Employee.objects.all()
        self.assertEqual(len(employees), 1)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['admin_form'].is_valid())
        self.assertEqual(response.context['admin_form'].errors, {
            'username': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'caffe/new.html')
