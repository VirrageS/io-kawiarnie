from datetime import date

from django.test import TestCase

from caffe.models import Caffe
from employees.models import Employee

from .models import Position, WorkedHours


class PositionModelTest(TestCase):
    """Position model tests."""

    def setUp(self):
        """Prepare database for tests."""

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

    def test_create(self):
        """Test if Position create succeded."""

        self.assertEqual(Position.objects.count(), 0)

        Position.objects.create(
            name="Zmywak",
            caffe=self.kafo
        )

        self.assertEqual(Position.objects.count(), 1)

        Position.objects.create(
            name="Kasa",
            caffe=self.kafo
        )

        position3 = Position.objects.create(
            name="Kelner",
            caffe=self.kafo
        )

        self.assertEqual(Position.objects.count(), 3)

        position3.delete()

        self.assertEqual(Position.objects.count(), 2)

        Position.objects.create(name="Kelner", caffe=self.kafo)
        Position.objects.create(name="Kelner", caffe=self.filtry)

        self.assertEqual(Position.objects.count(), 4)

    def test_create_fail(self):
        """Test if Position create failed."""

        Position.objects.create(name="Zmywak", caffe=self.kafo)

        with self.assertRaises(Exception):
            Position.objects.create(name="Zmywak", caffe=self.kafo)

        with self.assertRaises(Exception):
            Position.objects.create(name="", caffe=self.kafo)

        Position.objects.create(name="Zmywak", caffe=self.filtry)
        with self.assertRaises(Exception):
            Position.objects.create(name="", caffe=self.filtry)

class WorkedHoursModelTest(TestCase):
    """WorkedHours model tests."""

    def setUp(self):
        """Set up data to tests."""

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

        self.cleaning = Position.objects.create(name="Zmywak", caffe=self.kafo)
        self.cleaning_f = Position.objects.create(name="Z", caffe=self.filtry)

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
        self.user_f = Employee.objects.create(
            username="u3",
            first_name="f_u3",
            last_name="l_u3",
            telephone_number="31312",
            email="he@he.he",
            favorite_coffee="Rozpuszczalna",
            caffe=self.filtry
        )

    def test_create(self):
        """Test creation of objects."""

        worked_hours1 = WorkedHours.objects.create(
            start_time="15:00",
            end_time="16:00",
            date=date.today(),
            position=self.cleaning,
            employee=self.user1,
            caffe=self.kafo
        )

        self.assertEqual(1, WorkedHours.objects.count())

        worked_hours2 = WorkedHours.objects.create(
            start_time="17:00",
            end_time="18:00",
            date=date.today(),
            position=self.cleaning,
            employee=self.user1,
            caffe=self.kafo
        )

        WorkedHours.objects.create(
            start_time="20:00",
            end_time="21:00",
            date=date.today(),
            position=self.cleaning,
            employee=self.user1,
            caffe=self.kafo
        )

        self.assertEqual(WorkedHours.objects.count(), 3)

        worked_hours1.delete()
        worked_hours2.delete()

        self.assertEqual(WorkedHours.objects.count(), 1)

        WorkedHours.objects.create(
            start_time="20:30",
            end_time="21:30",
            date=date.today(),
            position=self.cleaning,
            employee=self.user2,
            caffe=self.kafo
        )

        self.assertEqual(2, WorkedHours.objects.count())
        self.assertEqual(
            1,
            WorkedHours.objects.filter(employee=self.user2).count()
        )
        self.assertEqual(
            1,
            WorkedHours.objects.filter(employee=self.user1).count()
        )

    def test_create_hours_fail(self):
        """Check cases in which WorkedHours should fail."""

        WorkedHours.objects.create(
            start_time="20:30",
            end_time="21:30",
            date=date.today(),
            position=self.cleaning,
            employee=self.user2,
            caffe=self.kafo
        )

        with self.assertRaises(Exception):
            WorkedHours.objects.create(
                start_time="20:30",
                end_time="21:30",
                date=date.today(),
                position=self.cleaning,
                employee=self.user_f,
                caffe=self.kafo
            )

        with self.assertRaises(Exception):
            WorkedHours.objects.create(
                start_time="20:30",
                end_time="21:30",
                date=date.today(),
                position=self.cleaning_f,
                employee=self.user2,
                caffe=self.kafo
            )

        with self.assertRaises(Exception):
            WorkedHours.objects.create(
                start_time="20:30",
                end_time="21:30",
                date=date.today(),
                position=self.cleaning,
                employee=self.user2,
                caffe=self.filtry
            )
