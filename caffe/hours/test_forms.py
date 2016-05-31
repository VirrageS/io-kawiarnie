"""Reports forms tests module."""
# -*- encoding: utf-8 -*-

from django.test import TestCase

from .forms import WorkedHoursForm
from .models import WorkedHours

from employees.models import Employee

from datetime import date, timedelta


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

    def test_workedhours(self):
        """Check validation - should pass."""
        form_correct = WorkedHoursForm({
            'start_time': "15:00",
            'end_time': "16:00",
            'date': date.today()
        })

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

        form_correct = WorkedHoursForm({
            'start_time': "15:30",
            'end_time': "16:50",
            'date': date.today() - timedelta(1)
        })

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

    def test_workedhours_fail(self):
        """Check validation - should not pass."""

        form_correct = WorkedHoursForm({
            'start_time': "15:00",
            'end_time': "16:00",
            'date': date.today()
        })

        self.assertTrue(form_correct.is_valid())
        form_correct.save()


        form_incorrect = WorkedHoursForm({
            'start_time': "14:50",
            'end_time': "14:30",
            'date': date.today()
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm({
            'start_time': "15:30",
            'end_time': "16:30",
            'date': date.today()
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()


        form_incorrect = WorkedHoursForm({
            'start_time': "14:30",
            'end_time': "17:30",
            'date': date.today()
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()


        form_incorrect = WorkedHoursForm({
            'start_time': "15:30",
            'end_time': "15:40",
            'date': date.today()
        })

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()