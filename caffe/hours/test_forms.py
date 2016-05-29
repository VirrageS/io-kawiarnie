"""Reports forms tests module."""
# -*- encoding: utf-8 -*-

from django.test import TestCase

from .forms import WorkedHoursFrom
from .models import WorkedHours


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

        })