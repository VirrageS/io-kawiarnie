"""Test module for views of the employee utility."""

from django.core.urlresolvers import NoReverseMatch, reverse
from django.test import Client, TestCase

from .forms import EmployeeForm
from .models import Employee


class EmployeeViewsTests(TestCase):
    """Test all views of the Employee model."""

    def setUp(self):
        """Initiate everything needed in tests."""

        self.client = Client()
        self.emp1 = Employee.objects.create(username='marta', password='pass')
        self.emp2 = Employee.objects.create(username='szkarta', password='passtoo')

    def test_show_all_employees(self):
        """Check if employees are all displayed properly."""

        response = self.client.get(reverse('show_all_employees'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/all.html')

        self.assertEqual(len(response.context['employees']), 2)
        self.assertIn(self.emp1, response.context['employees'])
        self.assertIn(self.emp2, response.context['employees'])

    def test_employees_edit(self):
        """Check if editing employees works as intended."""

        response = self.client.get(reverse('edit_employee',  args=(42,)))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('edit_employee', args=(self.emp1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/edit.html')
        self.assertIsInstance(response.context['form'], EmployeeForm)
        self.assertEqual(response.context['employee'], self.emp1)
