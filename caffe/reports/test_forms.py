# -*- encoding: utf-8 -*-

from django.test import TestCase
from django.utils import timezone
from django.db import transaction
from django import forms

from .models import Report, Category, Product, Unit, FullProduct
from .forms import CategoryForm, UnitForm, ProductForm
from .forms import FullProductForm, ReportForm

class CategoryFormTest(TestCase):

    def test_category(self):
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


class FullProductFormTest(TestCase):

    def setUp(self):
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
        p1 = Product.objects.get(name="product1")
        p2 = Product.objects.get(name="product2")

        form_correct = FullProductForm({
            'product': p1.id,
            'amount': 10
        })

        self.assertTrue(form_correct.is_valid())

        form_correct = FullProductForm({
            'product': p2.id,
            'amount': 10000000
        })

        self.assertTrue(form_correct.is_valid())

        p2.delete()

        form_incorrect = FullProductForm({
            'product': p2.id,
            'amount': 10
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm({
            'product': '',
            'amount': 10
        })

        self.assertFalse(form_incorrect.is_valid())

        '''
        form_incorrect = FullProductForm({
            'product':'1',
            'amount':10
        })

        self.assertFalse(form_incorrect.is_valid())
        '''

        form_incorrect = FullProductForm({
            'product': p1.id,
            'amount': -10
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm({
            'no_such': 'field'
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = FullProductForm({
            'product': 1231,
            'amount': 100
        })

        self.assertFalse(form_incorrect.is_valid())


class UnitFormTest(TestCase):

    def test_unit_form(self):

        form_correct = UnitForm({
            "name": "correct"
        })

        self.assertTrue(form_correct.is_valid())

        form_incorrect = UnitForm({
            'no_such': 'field'
        })

        self.assertFalse(form_incorrect.is_valid())

        form_correct = UnitForm({
            'name': 'Category is correct'
        })

        self.assertTrue(form_correct.is_valid())

        form_correct = UnitForm({
            'name': 'This.is.correct123!@#$%"^&"*():?>M'
        })

        self.assertTrue(form_correct.is_valid())


class ProductFormTest(TestCase):

    def setUp(self):
        Category.objects.create(name="first")
        Category.objects.create(name="second")

        Unit.objects.create(name="gram")
        Unit.objects.create(name="liter")

    def test_product_form(self):
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


class ReportFormTest(TestCase):

    def setUp(self):
        first_cat = Category.objects.create(name="first")
        second_cat = Category.objects.create(name="second")

        gram = Unit.objects.create(name="gram")
        liter = Unit.objects.create(name="liter")

        p1 = Product.objects.create(
            name="product1",
            category=first_cat,
            unit=gram
        )
        p2 = Product.objects.create(
            name="product2",
            category=first_cat,
            unit=liter
        )
        p3 = Product.objects.create(
            name="product3",
            category=second_cat,
            unit=gram
        )
        p4 = Product.objects.create(
            name="product4",
            category=second_cat,
            unit=liter
        )

        fp1 = FullProduct.objects.create(
            product=p1,
            amount=10
        )

        fp2 = FullProduct.objects.create(
            product=p2,
            amount=100
        )

        fp3 = FullProduct.objects.create(
            product=p3,
            amount=0
        )

        fp4 = FullProduct.objects.create(
            product=p4,
            amount=1000
        )

    def test_report(self):
        all_fp =  [x.id for x in FullProduct.objects.all()]
        form_correct = ReportForm({
            'full_products':all_fp
        })

        self.assertTrue(form_correct.is_valid())

        p1 = Product.objects.get(name="product1")
        fp5 = FullProduct.objects.create(
            product=p1,
            amount=10
        )

        fp5.save()

        all_fp =  [x.id for x in FullProduct.objects.all()[:2]]
        form_correct = ReportForm({
            'full_products':all_fp
        })

        self.assertTrue(form_correct.is_valid())
