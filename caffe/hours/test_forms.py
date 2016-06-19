# -*- encoding: utf-8 -*-

from datetime import date, timedelta

from django.test import TestCase

from caffe.models import Caffe
from employees.models import Employee

from .forms import WorkedHoursForm, PositionForm
from .models import Position


class PositionFormTest(TestCase):
    """Tests Position form."""

    def setUp(self):
        """Initialize all models needed for further tests."""

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

    def test_position_form_correct(self):
        """Check possible cases when PositionForm is correct."""

        form_correct = PositionForm(
            {'name': 'Zmywak'},
            caffe=self.kafo
        )
        self.assertTrue(form_correct.is_valid())

        position = form_correct.save()
        self.assertEqual(position.name, 'Zmywak')
        self.assertEqual(position.caffe, self.kafo)

    def test_position_form_incorrect(self):
        """Check possible cases when PositionForm is not correct."""

        form_incorrect = PositionForm(
            {'name': ''},
            caffe=self.kafo
        )
        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = PositionForm(
            {'name': '      '},
            caffe=self.kafo
        )

        self.assertFalse(form_incorrect.is_valid())

    def test_position_same_name(self):
        """Check if Position with same name cannot be created."""

        Position.objects.create(name='Zmywak', caffe=self.kafo)
        form_incorrect = PositionForm(
            {'name': 'Zmywak'},
            caffe=self.kafo
        )
        self.assertFalse(form_incorrect.is_valid())

        form_correct = PositionForm(
            {'name': 'Zmywak'},
            caffe=self.filtry
        )
        self.assertTrue(form_correct.is_valid())

    def test_position_form_instance(self):
        """Check Position form with loaded instance."""

        position = Position.objects.create(name='Zmywak', caffe=self.kafo)

        form_correct = PositionForm(
            {'name': 'Barista'},
            instance=position,
            caffe=self.kafo
        )

        self.assertIsInstance(form_correct.instance, Position)
        self.assertEqual(form_correct.instance.id, position.id)

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

        get_position = Position.objects.get(id=position.id)
        self.assertEqual(get_position.name, 'Barista')
        self.assertEqual(get_position.caffe, self.kafo)


class WorkedHoursFormTest(TestCase):
    """Tests of WorkedHoursForm."""

    def setUp(self):
        """Set up data to tests."""

        self.kafo = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        self.user1 = Employee.objects.create(
            username="u1",
            first_name="f_u1",
            last_name="l_u1",
            telephone_number="31312",
            email="he@he.he",
            favorite_coffee="Rozpuszczalna",
            caffe=self.kafo
        )

        self.user2 = Employee.objects.create(
            username="u2",
            first_name="f_u2",
            last_name="l_u2",
            telephone_number="31312",
            email="he@he.he",
            favorite_coffee="Rozpuszczalna",
            caffe=self.kafo
        )

        self.barista = Position.objects.create(name='Barista', caffe=self.kafo)
        self.cleaning = Position.objects.create(name='Sprzątanie',
                                                caffe=self.kafo)

    def test_workedhours(self):
        """Check validation - should pass."""

        form_correct = WorkedHoursForm(
            {
                'start_time': "15:00",
                'end_time': "16:00",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user1,
            caffe=self.kafo
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
            employee=self.user1,
            caffe=self.kafo
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
            employee=self.user1,
            caffe=self.kafo
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
            employee=self.user2,
            caffe=self.kafo
        )

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

    def test_workedhours_fail(self):
        """Check validation - should not pass."""

        form_correct = WorkedHoursForm(
            {
                'start_time': "15:00",
                'end_time': "16:00",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user2,
            caffe=self.kafo
        )

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

        form_incorrect = WorkedHoursForm(
            {
                'start_time': "14:50",
                'end_time': "14:30",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user2,
            caffe=self.kafo
        )

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm(
            {
                'start_time': "15:30",
                'end_time': "16:30",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user2,
            caffe=self.kafo
        )

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm(
            {
                'start_time': "14:30",
                'end_time': "17:30",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user2,
            caffe=self.kafo
        )

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm(
            {
                'start_time': "15:30",
                'end_time': "15:40",
                'date': date.today(),
                'position': self.barista.id
            },
            employee=self.user2,
            caffe=self.kafo
        )

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()

        form_incorrect = WorkedHoursForm(
            {
                'start_time': "20:30",
                'end_time': "21:40",
                'date': date.today(),
                'position': ''
            },
            employee=self.user2,
            caffe=self.kafo
        )

        self.assertFalse(form_incorrect.is_valid())

        with self.assertRaises(Exception):
            form_incorrect.save()
