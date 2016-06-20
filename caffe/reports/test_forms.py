# -*- encoding: utf-8 -*-

from django.test import TestCase

from caffe.models import Caffe
from employees.models import Employee

from .forms import (CategoryForm, FullProductForm, ProductForm, ReportForm,
                    UnitForm)
from .models import Category, Product, Unit


class CategoryFormTest(TestCase):
    """Tests of CategoryForm."""

    def setUp(self):
        """Test data setup."""

        self.caffe = Caffe.objects.create(
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

    def test_category(self):
        """Check validation."""

        form_incorrect = CategoryForm(
            {'name': ''},
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = CategoryForm(
            {'no_such': 'field'},
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        form_correct = CategoryForm(
            {'name': 'Category is correct'},
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        form_correct = CategoryForm(
            {'name': 'This.is.correct123!@#$%"^&"*():?>M'},
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        # test no caffe
        with self.assertRaises(Exception):
            CategoryForm({'name': "category"})

    def test_name_validation(self):
        """Check name validation."""

        Category.objects.create(name='Correct', caffe=self.filtry)

        form_correct = CategoryForm(
            {'name': 'Correct'},
            caffe=self.caffe
        )
        self.assertTrue(form_correct.is_valid())

        # invalid name
        Category.objects.create(name='Correct', caffe=self.caffe)

        form_incorrect = CategoryForm(
            {'name': 'Correct'},
            caffe=self.caffe
        )
        self.assertFalse(form_incorrect.is_valid())


class UnitFormTest(TestCase):
    """UnitForm tets."""

    def setUp(self):
        """Test data setup."""

        self.caffe = Caffe.objects.create(
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

    def test_unit_form(self):
        """Validation tests."""

        form_correct = UnitForm(
            {"name": "correct"},
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        form_incorrect = UnitForm(
            {'no_such': 'field'},
            caffe=self.caffe
        )

        # should not pass with not-existent
        self.assertFalse(form_incorrect.is_valid())

        form_correct = UnitForm(
            {'name': 'Category is correct'},
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        form_correct = UnitForm(
            {'name': 'This.is.correct123!@#$%"^&"*():?>M'},
            caffe=self.caffe
        )

        # should pass with ascii characters
        self.assertTrue(form_correct.is_valid())

        # test no caffe
        with self.assertRaises(Exception):
            UnitForm({'name': 'Unit'})

    def test_unit_same_name(self):
        """Check if Unit with same name is properly handled."""

        Unit.objects.create(name='Correct', caffe=self.filtry)

        form_correct = UnitForm(
            {'name': 'Correct'},
            caffe=self.caffe
        )
        self.assertTrue(form_correct.is_valid())

        # invalid name
        Unit.objects.create(name='Correct', caffe=self.caffe)

        form_incorrect = UnitForm(
            {'name': 'Correct'},
            caffe=self.caffe
        )
        self.assertFalse(form_incorrect.is_valid())


class ProductFormTest(TestCase):
    """ProductForm tests."""

    def setUp(self):
        """Test data setup."""

        self.caffe = Caffe.objects.create(
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

        self.cat_first = Category.objects.create(
            name="first",
            caffe=self.caffe
        )
        self.cat_second = Category.objects.create(
            name="second",
            caffe=self.caffe
        )
        self.cat_first_f = Category.objects.create(
            name="second",
            caffe=self.filtry
        )

        self.gram = Unit.objects.create(name="gram", caffe=self.caffe)
        self.liter = Unit.objects.create(name="liter", caffe=self.caffe)
        self.liter_f = Unit.objects.create(name="liter", caffe=self.filtry)

    def test_product_form(self):
        """Check validation."""

        form_correct = ProductForm(
            {
                'name': 'Correct',
                'category': self.cat_first.id,
                'unit': self.gram.id
            },
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        form_correct = ProductForm(
            {
                'name': 'Correct',
                'category': self.cat_second.id,
                'unit': self.liter.id
            },
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        form_incorrect = ProductForm(
            {
                'name': "This is to long name!@dg#d!%#@fd%$f1c@%!#$!"
                        "#!@$#@%@#%$@%!#FaSDCARADASFVXT#Q%#$@!$!@$"
                        "#FWB THRYu%#$^u6uyj6#$Tga5%@4rFEtwGEQWEFZ"
                        "eQEQWvgrtuT(;p8O8olkTU8Uyhdasa213r63634e5",
                'category': self.cat_second.id,
                'unit': self.liter.id
            },
            caffe=self.caffe
        )

        # too long name
        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = ProductForm(
            {
                'name': '',
                'category': self.cat_second.id,
                'unit': self.liter.id
            },
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = ProductForm(
            {'name': 'name', 'category': -1, 'unit': self.liter.id},
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = ProductForm(
            {'name': 'name', 'category': self.cat_second.id, 'unit': 100},
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        self.cat_second.delete()

        form_incorrect = ProductForm(
            {
                'name': 'Correct',
                'category': self.cat_second.id,
                'unit': self.liter.id
            },
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        self.gram.delete()

        form_incorrect = ProductForm(
            {
                'name': 'Correct',
                'category': self.cat_first.id,
                'unit': self.gram.id
            },
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        # test no caffe
        with self.assertRaises(Exception):
            ProductForm({
                'name': 'Pr',
                'category': self.cat_second.id,
                'unit': self.liter.id
            })

    def test_product_same_name(self):
        """Check if product with same name is properly handled."""

        Product.objects.create(
            name='Correct',
            category=self.cat_first_f,
            unit=self.liter_f,
            caffe=self.filtry
        )

        form_correct = ProductForm(
            {
                'name': 'Correct',
                'category': self.cat_second.id,
                'unit': self.liter.id
            },
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        Product.objects.create(
            name='Correct',
            category=self.cat_second,
            unit=self.liter,
            caffe=self.caffe
        )

        form_incorrect = ProductForm(
            {
                'name': 'Correct',
                'category': self.cat_second.id,
                'unit': self.liter.id
            },
            caffe=self.caffe
        )
        self.assertFalse(form_incorrect.is_valid())


class FullProductFormTest(TestCase):
    """FullProductForm tests."""

    def setUp(self):
        """Initialize data for further FullProductForm tests."""

        self.caffe = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        first_cat = Category.objects.create(name="first", caffe=self.caffe)
        second_cat = Category.objects.create(name="second", caffe=self.caffe)

        gram = Unit.objects.create(name="gram", caffe=self.caffe)
        liter = Unit.objects.create(name="liter", caffe=self.caffe)

        Product.objects.create(
            name="product1",
            category=first_cat,
            unit=gram,
            caffe=self.caffe
        )

        Product.objects.create(
            name="product2",
            category=second_cat,
            unit=liter,
            caffe=self.caffe
        )

    def test_full_product(self):
        """Check validation and adding/deleting products."""
        product1 = Product.objects.get(name="product1")
        product2 = Product.objects.get(name="product2")

        form_correct = FullProductForm(
            {'product': product1.id, 'amount': 10},
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        form_correct = FullProductForm(
            {'product': product2.id, 'amount': 10000000},
            caffe=self.caffe
        )

        self.assertTrue(form_correct.is_valid())

        product2.delete()

        form_incorrect = FullProductForm(
            {'product': product2.id, 'amount': 10},
            caffe=self.caffe
        )

        # should not pass with deleted product
        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm(
            {'product': '', 'amount': 10},
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm(
            {'product': product1.id, 'amount': -10},
            caffe=self.caffe
        )

        # amount should not be negative
        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm(
            {'no_such': 'field'},
            caffe=self.caffe
        )

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm(
            {'product': 1231, 'amount': 100},
            caffe=self.caffe
        )

        # not existing product id
        self.assertFalse(form_incorrect.is_valid())

        # test no caffe
        with self.assertRaises(Exception):
            FullProductForm({'product': product1.id, 'amount': 100})


class ReportFormTest(TestCase):
    """Report tests."""

    def setUp(self):
        """Initialize data for further Report tests."""

        self.caffe = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        self.user = Employee.objects.create(
            username='admin',
            password='admin',
            caffe=self.caffe
        )

    def test_report(self):
        """Check validation on ReportForm."""

        # check no caffe
        with self.assertRaises(Exception):
            ReportForm({}, creator=self.user)

        # check no employee
        with self.assertRaises(Exception):
            ReportForm({}, caffe=self.caffe)

        # validate okay
        form = ReportForm({}, caffe=self.caffe, creator=self.user)
        self.assertTrue(form.is_valid())
