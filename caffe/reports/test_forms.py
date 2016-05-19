"""Reports forms tests module."""
# -*- encoding: utf-8 -*-

from django.test import TestCase

from .forms import CategoryForm, FullProductForm, ProductForm, UnitForm
from .models import Category, Product, Unit


class CategoryFormTest(TestCase):
    """Tests of CategoryForm."""

    def test_category(self):
        """Check validation."""
        form_incorrect = CategoryForm({
            'name': ''
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = CategoryForm({
            'no_such': 'field'
        })

        self.assertFalse(form_incorrect.is_valid())

        form_correct = CategoryForm({
            'name': 'Category is correct'
        })

        self.assertTrue(form_correct.is_valid())

        form_correct = CategoryForm({
            'name': 'This.is.correct123!@#$%"^&"*():?>M'
        })

        self.assertTrue(form_correct.is_valid())


class UnitFormTest(TestCase):
    """UnitForm tets."""

    def test_unit_form(self):
        """Validation tests."""
        form_correct = UnitForm({
            "name": "correct"
        })

        self.assertTrue(form_correct.is_valid())

        form_incorrect = UnitForm({
            'no_such': 'field'
        })

        # should not pass with not-existent
        self.assertFalse(form_incorrect.is_valid())

        form_correct = UnitForm({
            'name': 'Category is correct'
        })

        self.assertTrue(form_correct.is_valid())

        form_correct = UnitForm({
            'name': 'This.is.correct123!@#$%"^&"*():?>M'
        })

        # should pass with ascii characters
        self.assertTrue(form_correct.is_valid())


class ProductFormTest(TestCase):
    """ProductForm tests."""

    def setUp(self):
        """Test setup data."""
        Category.objects.create(name="first")
        Category.objects.create(name="second")

        Unit.objects.create(name="gram")
        Unit.objects.create(name="liter")

    def test_product_form(self):
        """Check validation."""

        first_cat = Category.objects.get(name="first")
        second_cat = Category.objects.get(name="second")

        gram = Unit.objects.get(name="gram")
        liter = Unit.objects.get(name="liter")

        form_correct = ProductForm({
            'name': 'Some correct product',
            'category': first_cat.id,
            'unit': gram.id
        })

        self.assertTrue(form_correct.is_valid())

        form_correct = ProductForm({
            'name': 'Some correct product',
            'category': second_cat.id,
            'unit': liter.id
        })

        self.assertTrue(form_correct.is_valid())

        form_incorrect = ProductForm({
            'name': "This is to long name!@dg#d!%#@fd%$f1c@%!#$!"
                    "#!@$#@%@#%$@%!#FaSDCARADASFVXT#Q%#$@!$!@$"
                    "#FWB THRYu%#$^u6uyj6#$Tga5%@4rFEtwGEQWEFZ"
                    "eQEQWvgrtuT(;p8O8olkTU8Uyhdasa213r63634e5",
            'category': second_cat.id,
            'unit': liter.id
        })

        # too long name
        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = ProductForm({
            'name': '',
            'category': second_cat.id,
            'unit': liter.id
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = ProductForm({
            'name': 'name',
            'category': -1,
            'unit': liter.id
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = ProductForm({
            'name': 'name',
            'category': second_cat.id,
            'unit': 100
        })

        self.assertFalse(form_incorrect.is_valid())

        second_cat.delete()

        form_incorrect = ProductForm({
            'name': 'Some correct product',
            'category': second_cat.id,
            'unit': liter.id
        })

        self.assertFalse(form_incorrect.is_valid())

        gram.delete()

        form_incorrect = ProductForm({
            'name': 'Some correct product',
            'category': first_cat.id,
            'unit': gram.id
        })

        self.assertFalse(form_incorrect.is_valid())


class FullProductFormTest(TestCase):
    """FullProductForm tests."""

    def setUp(self):
        """Initialize data for further FullProductForm tests."""

        first_cat = Category.objects.create(name="first")
        second_cat = Category.objects.create(name="second")

        gram = Unit.objects.create(name="gram")
        liter = Unit.objects.create(name="liter")

        Product.objects.create(
            name="product1",
            category=first_cat,
            unit=gram
        )

        Product.objects.create(
            name="product2",
            category=second_cat,
            unit=liter
        )

    def test_full_product(self):
        """Check validation and adding/deleting products."""
        product1 = Product.objects.get(name="product1")
        product2 = Product.objects.get(name="product2")

        form_correct = FullProductForm({
            'product': product1.id,
            'amount': 10
        })

        self.assertTrue(form_correct.is_valid())

        form_correct = FullProductForm({
            'product': product2.id,
            'amount': 10000000
        })

        self.assertTrue(form_correct.is_valid())

        product2.delete()

        form_incorrect = FullProductForm({
            'product': product2.id,
            'amount': 10
        })

        # should not pass with deleted product
        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm({
            'product': '',
            'amount': 10
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm({
            'product': product1.id,
            'amount': -10
        })

        # amount should not be negative
        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm({
            'no_such': 'field'
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm({
            'product': 1231,
            'amount': 100
        })

        # not existing product id
        self.assertFalse(form_incorrect.is_valid())
