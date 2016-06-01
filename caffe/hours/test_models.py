from datetime import date

from django.test import TestCase

from employees.models import Employee

from .models import WorkedHours


class WorkedHoursModelTest(TestCase):
    """WorkedHours model tests."""

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

    def test_create(self):
        """Test creation of objects."""
        worked_hours1 = WorkedHours.objects.create(
            start_time="15:00",
            end_time="16:00",
            date=date.today(),
            employee=self.user1
        )

        self.assertEqual(1, WorkedHours.objects.count())

        worked_hours2 = WorkedHours.objects.create(
            start_time="17:00",
            end_time="18:00",
            date=date.today(),
            employee=self.user1
        )

        WorkedHours.objects.create(
            start_time="20:00",
            end_time="21:00",
            date=date.today(),
            employee=self.user1
        )

        self.assertEqual(WorkedHours.objects.count(), 3)

        worked_hours1.delete()
        worked_hours2.delete()

        self.assertEqual(WorkedHours.objects.count(), 1)

        WorkedHours.objects.create(
            start_time="20:30",
            end_time="21:30",
            date=date.today(),
            employee=self.user2
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
