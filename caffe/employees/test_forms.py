"""Reports forms tests module."""
# -*- encoding: utf-8 -*-

from django.test import TestCase

from .forms import EmployeeForm
from .models import Employee

from django.contrib.auth.models import Group


class EmployeeFormTest(TestCase):
    """Test empoloyee form."""

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

    def test_validation(self):
        """Check validation of employee form."""

        valid = EmployeeForm({
            'username': 'u2',
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'groups': [self.group1.id, ],
            'email': 'he@he.he',
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'haslohaslo'
        })

        self.assertTrue(valid.is_valid())

        valid = EmployeeForm({
            'username': 'u2',
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'email': 'he@he.he',
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'haslohaslo'
        })

        self.assertTrue(valid.is_valid())

        not_valid = EmployeeForm({
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'email': 'he@he.he',
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'haslohaslo'
        })

        # no username
        self.assertFalse(not_valid.is_valid())

        not_valid = EmployeeForm({
            'username': 'u1',
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'email': 'he@he.he',
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'haslohaslo'
        })

        # username exists already
        self.assertFalse(not_valid.is_valid())

        not_valid = EmployeeForm({
            'username': 'u1',
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'email': 'he',
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'haslohaslo'
        })

        # wrong email adress
        self.assertFalse(not_valid.is_valid())

        not_valid = EmployeeForm({
            'username': 'u4',
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'email': 'he@he.he',
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'hasloinne'
        })

        # passwords differ
        self.assertFalse(not_valid.is_valid())

        not_valid = EmployeeForm({
            'username': '',
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'email': 'he@he.he',
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'haslohaslo'
        })

        # empty username
        self.assertFalse(not_valid.is_valid())

        not_valid = EmployeeForm({
            'username': 'useruser',
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'email': 'he@he.he',
            'groups': [-1, -2],
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'haslohaslo'
        })

        # wrong groups
        self.assertFalse(not_valid.is_valid())