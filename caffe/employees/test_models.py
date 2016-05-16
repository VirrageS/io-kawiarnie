"""Employees models tests module."""
# -*- encoding: utf-8 -*-

from django.test import TestCase

from .models import Employee

from django.contrib.auth.models import Group


class EmployeeModelTest(TestCase):
    """Employee model tests."""

    def setUp(self):
        """Set up data to tests."""
        self.group1 = Group.objects.create(
            name="grupa1")

        self.group2 = Group.objects.create(
            name="grupa2")

        self.user1 = Employee.objects.create(
            username="u1",
            first_name="f_u1",
            last_name="l_u1",
            telephone_number="31312",
            email="he@he.he",
            favorite_coffee="Rozpuszczalna"
        )

        self.user1.groups.add(self.group1)
        self.user1.groups.add(self.group2)

    def test_create(self):
        """Test creation of objects."""
        self.assertEqual(2, Group.objects.count())

        self.assertEqual(1, Employee.objects.count())

        user2 = Employee.objects.create(
            username="u2",
            first_name="f_u2",
            last_name="l_u2",
            telephone_number="31312",
            email="he@he.he",
            favorite_coffee="Rozpuszczalna"
        )

        self.assertEqual(2, Employee.objects.count())

        user2.delete()

        self.assertEqual(1, Employee.objects.count())

        with self.assertRaises(Exception):
            Employee.objects.create(
                username="u1",
                first_name="l_u2",
                last_name="l_u2",
                telephone_number="31312",
                email="he@he.he",
                favorite_coffee="Rozpuszczalna"
            )

        with self.assertRaises(Exception):
            Employee.objects.create(
                username="",
                first_name="l_u2",
                last_name="l_u2",
                telephone_number="31312",
                email="he@he.he",
                favorite_coffee="Rozpuszczalna"
            )
