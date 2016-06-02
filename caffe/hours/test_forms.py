# -*- encoding: utf-8 -*-

from datetime import date, timedelta

from django.test import TestCase

from employees.models import Employee

from .forms import WorkedHoursForm
from .models import Position


class WorkedHoursFormTest(TestCase):
    """Tests of WorkedHoursForm."""

    def setUp(self):
        """Set up data to tests."""

        self.user1 = Employee.objects.create(
            username="u1",
            first_name="f_u1",
            last_name="l_u1",
            telephone_number="31312",
            email="he@he.he",
            favorite_coffee="Rozpuszczalna"
        )

        self.user2 = Employee.objects.create(
            username="u2",
            first_name="f_u2",
            last_name="l_u2",
            telephone_number="31312",
            email="he@he.he",
            favorite_coffee="Rozpuszczalna"
        )

        self.barista = Position.objects.create(name='Barista')
        self.cleaning = Position.objects.create(name='Sprzątanie')

    def test_workedhours(self):
        """Check validation - should pass."""

        form_correct = WorkedHoursForm(
            {
                'start_time': "15:00",
                'end_time': "16:00",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user1
        )

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

        form_correct = WorkedHoursForm(
            {
                'start_time': "15:30",
                'end_time': "16:50",
                'date': date.today() - timedelta(1),
                'position': self.barista.id
            },
            employee=self.user1
        )

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

    def test_workedhours_two_employees(self):
        """Test WorkedHours forms for two employees."""
        form_correct = WorkedHoursForm(
            {
                'start_time': "15:00",
                'end_time': "16:00",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user1
        )

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

        form_correct = WorkedHoursForm(
            {
                'start_time': "15:30",
                'end_time': "16:50",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user2
        )

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

    def test_workedhours_fail(self):
        """Check validation - should not pass."""

        form_correct = WorkedHoursForm({
            'start_time': "15:00",
            'end_time': "16:00",
            'date': date.today(),
            'position': self.barista.id
        })

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

        form_incorrect = WorkedHoursForm({
            'start_time': "14:50",
            'end_time': "14:30",
            'date': date.today(),
            'position': self.barista.id
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm({
            'start_time': "15:30",
            'end_time': "16:30",
            'date': date.today(),
            'position': self.barista.id
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm({
            'start_time': "14:30",
            'end_time': "17:30",
            'date': date.today(),
            'position': self.barista.id
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm({
            'start_time': "15:30",
            'end_time': "15:40",
            'date': date.today(),
            'position': self.barista.id
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm({
            'start_time': "20:30",
            'end_time': "21:40",
            'date': date.today(),
            'position': ''
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()
