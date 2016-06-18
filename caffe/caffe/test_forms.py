"""Caffe forms tests module."""
# -*- encoding: utf-8 -*-

from django.test import TestCase

from .forms import CaffeForm
from .models import Caffe
from employees.forms import EmployeeForm
from employees.models import Employee


class CaffeFormTest(TestCase):
    """Test caffe form."""

    def setUp(self):
        """Set data for tests."""
        
        employee_form = EmployeeForm({
            'username': 'u2',
            'first_name': 'fu1',
            'last_name': 'fu2',
            'telephone_number': '312313',
            'email': 'he@he.he',
            'favorite_coffee': 'black',
            'password1': 'haslohaslo',
            'password2': 'haslohaslo'
        })

        self.employee = employee_form.save()

    def test_create(self):
        """Check creation of valid caffe."""

        valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'00-000',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertTrue(valid.is_valid())
        caffe = valid.save(commit=False)
        caffe.creator = self.employee
        caffe.save()
        self.assertEquals(Caffe.objects.count(), 1)

        valid = CaffeForm({
            'name':'Caffe2',
            'city':'SanCaffe2',
            'street':'CaffeStreet2',
            'postal_code':'00-100',
            'building_number':'50a',
            'house_number':'40'
        })

        self.assertTrue(valid.is_valid())
        caffe = valid.save(commit=False)
        caffe.creator = self.employee
        caffe.save()
        self.assertEquals(Caffe.objects.count(), 2)

        valid = CaffeForm({
            'name':'Caffe3',
            'city':'SanCaffe3',
            'street':'CaffeStreet3',
            'postal_code':'00-003',
            'building_number':'50'
        })

        self.assertTrue(valid.is_valid())
        caffe = valid.save(commit=False)
        caffe.creator = self.employee
        caffe.save()
        self.assertEquals(Caffe.objects.count(), 3)

    def test_name_unique(self):
        """Test if names of caffe are uniqe."""

        valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'00-000',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertTrue(valid.is_valid())
        caffe = valid.save(commit=False)
        caffe.creator = self.employee
        caffe.save()

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe2',
            'street':'CaffeStreet2',
            'postal_code':'00-100',
            'building_number':'50a',
            'house_number':'40'
        })

        self.assertFalse(not_valid.is_valid())

        with self.assertRaises(Exception):
            caffe = not_valid.save(commit=False)
            caffe.creator = self.employee
            caffe.save()

    def test_required_fields(self):
        """Test required fields."""

        not_valid = CaffeForm({
            'city':'SanCaffe2',
            'street':'CaffeStreet2',
            'postal_code':'00-100',
            'building_number':'50a',
            'house_number':'40'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'street':'CaffeStreet2',
            'postal_code':'00-100',
            'building_number':'50a',
            'house_number':'40'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe2',
            'postal_code':'00-100',
            'building_number':'50a',
            'house_number':'40'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe2',
            'street':'CaffeStreet2',
            'building_number':'50a',
            'house_number':'40'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe2',
            'street':'CaffeStreet2',
            'postal_code':'00-100',
            'house_number':'40'
        })

        self.assertFalse(not_valid.is_valid())

    def test_postal_code(self):
        """Test postal code validation."""

        valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'00-000',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertTrue(valid.is_valid())
        caffe = valid.save(commit=False)
        caffe.creator = self.employee
        caffe.save()
        self.assertEquals(Caffe.objects.count(), 1)

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'00000',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'00000',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'ab-bba',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'AB-CAS',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'##-###',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'1-234',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'12-24',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'112-242',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

        not_valid = CaffeForm({
            'name':'Caffe1',
            'city':'SanCaffe1',
            'street':'CaffeStreet1',
            'postal_code':'Caffe',
            'building_number':'50',
            'house_number':'100'
        })

        self.assertFalse(not_valid.is_valid())

