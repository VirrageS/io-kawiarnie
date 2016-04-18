# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone

from .models import Report, Category, Product, Unit, FullProduct

class CategoryModelTest(TestCase):

    def setUp(self):
        Category.objects.create(name="first")
        Category.objects.create(name="second")

    def test_category_name(self):
        c1 = Category(name="first")
        c2 = Category(name="second")

        self.assertTrue(c1.name != c2.name)
        self.assertEqual(c1.name, "first")
        self.assertEqual(c2.name, "second")
        self.assertRaises(Exception, Category.objects.create, name="first")
        self.assertRaises(Exception, Category.objects.create, name="second")


class UnitModelTest(TestCase):

    def setUp(self):
        Unit.objects.create(name="gram")
        Unit.objects.create(name="liter")

    def test_unit(self):
        u_gram = Unit.objects.get(name="gram")
        u_liter = Unit.objects.get(name="liter")
        u_gram2 = Unit.objects.get(name="gram")

        self.assertEqual(u_gram.id, u_gram2.id)
        self.assertRaises(Exception, Unit.objects.create, name="liter")


class ProductModelTest(TestCase):

    def setUp(self):
        Category.objects.create(name="first")
        Category.objects.create(name="second")

        Unit.objects.create(name="gram")
        Unit.objects.create(name="liter")

    def test_product(self):
        first_cat = Category.objects.get(name="first")
        second_cat = Category.objects.get(name="second")

        gram = Unit.objects.get(name="gram")
        liter = Unit.objects.get(name="liter")

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

        self.assertEqual(first_cat.product_set.count(), 2)
        p2.delete()
        self.assertEqual(first_cat.product_set.count(), 1)
        p3.category = first_cat
        p3.save()
        self.assertEqual(first_cat.product_set.count(), 2)
        self.assertEqual(second_cat.product_set.count(), 1)
        p3.category = second_cat
        p3.save()

        self.assertEqual(gram.product_set.count(), 2)
        p3.delete()
        self.assertEqual(gram.product_set.count(), 1)

        self.assertRaises(
            Exception,
            Product.objects.create,
            name="product1",
            category=first_cat,
            unit=gram
        )


class FullProductModelTest(TestCase):

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
            category=first_cat,
            unit=liter
        )
        Product.objects.create(
            name="product3",
            category=second_cat,
            unit=gram
        )
        Product.objects.create(
            name="product4",
            category=second_cat,
            unit=liter
        )

    def test_fullProduct(self):
        p1 = Product.objects.get(name="product1")
        p2 = Product.objects.get(name="product2")
        p3 = Product.objects.get(name="product3")
        p4 = Product.objects.get(name="product4")

        r1 = Report.objects.create(id=1)
        r2 = Report.objects.create(id=2)

        fp1 = FullProduct.objects.create(
            product=p1,
            amount=10,
            report=r1
        )

        fp2 = FullProduct.objects.create(
            product=p2,
            amount=100,
            report=r1
        )

        fp3 = FullProduct.objects.create(
            product=p3,
            amount=0,
            report=r2
        )

        fp4 = FullProduct.objects.create(
            product=p4,
            amount=1000,
            report=r2
        )

        self.assertEqual(fp1.product.name, "product1")
        self.assertEqual(fp2.amount, 100)
        self.assertEqual(fp2.report.id, r1.id)

        self.assertEqual(r2.full_products.count(), 2)
        fp4.delete()
        self.assertEqual(r2.full_products.count(), 1)

        self.assertEqual(r1.full_products.count(), 2)
        p2.delete()
        self.assertEqual(r1.full_products.count(), 1)

        fp1.amount = -1


class ReportModelTest(TestCase):

    def setUp(self):
        r1 = Report.objects.create(id=1)
        r2 = Report.objects.create(id=2)
        r3 = Report.objects.create(id=3)
        r4 = Report.objects.create(id=4)

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
            amount=10,
            report=r1

        )

        fp2 = FullProduct.objects.create(
            product=p2,
            amount=100,
            report=r2
        )

        fp3 = FullProduct.objects.create(
            product=p3,
            amount=0,
            report=r3
        )

        fp4 = FullProduct.objects.create(
            product=p4,
            amount=1000,
            report=r4
        )

    def test_created_on(self):
        now = timezone.now()
        r1 = Report.objects.get(id=1)
        self.assertEqual(Report.objects.count(), 4)

    def test_doubles(self):
        r1 = Report.objects.get(id=1)

        p = FullProduct.objects.first().product

        fp = FullProduct.objects.create(
            product=p,
            amount=1,
            report=r1
        )

        #self.assertRaises(Exception, fp.save)