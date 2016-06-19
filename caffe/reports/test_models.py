"""Reports models tests module."""
# -*- encoding: utf-8 -*-

from django.test import TestCase

from caffe.models import Caffe

from .models import Category, FullProduct, Product, Report, Unit


class CategoryModelTest(TestCase):
    """Category tests."""

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

        self.first = Category.objects.create(name="first", caffe=self.caffe)
        Category.objects.create(name="second", caffe=self.caffe)

    def test_category_name(self):
        """Chcek correctness of setting names."""
        category1 = Category(name="first")
        category2 = Category(name="second")

        self.assertTrue(category1.name != category2.name)
        self.assertEqual(category1.name, "first")
        self.assertEqual(category2.name, "second")

    def test_category_caffe(self):
        """Check if caffe is being set properly."""

        self.assertEqual(self.first.caffe, self.caffe)

        with self.assertRaises(Exception):
            Category.objects.create(name="first", caffe=self.caffe)

        with self.assertRaises(Exception):
            Category.objects.create(name="second", caffe=self.caffe)

        Category.objects.create(name="first", caffe=self.filtry)
        Category.objects.create(name="second", caffe=self.filtry)


class UnitModelTest(TestCase):
    """Unit tests."""

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

        self.gram = Unit.objects.create(name="gram", caffe=self.caffe)
        Unit.objects.create(name="liter", caffe=self.caffe)

    def test_unit(self):
        """Check creating units."""

        self.assertEqual(self.gram.name, "gram")
        self.assertEqual(self.gram.caffe, self.caffe)

        with self.assertRaises(Exception):
            Unit.objects.create(name="liter", caffe=self.caffe)

        Unit.objects.create(name="liter", caffe=self.filtry)


class ProductModelTest(TestCase):
    """Product tests."""

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

        self.cakes = Category.objects.create(name="cakes", caffe=self.caffe)
        self.second = Category.objects.create(name="second", caffe=self.caffe)
        self.cakes1 = Category.objects.create(name="cakes", caffe=self.filtry)

        self.gram = Unit.objects.create(name="gram", caffe=self.caffe)
        self.liter = Unit.objects.create(name="liter", caffe=self.caffe)
        self.gram1 = Unit.objects.create(name="gram", caffe=self.filtry)

    def test_product(self):
        """Check correctness of creating products and validation."""

        Product.objects.create(
            name="product1",
            category=self.cakes,
            unit=self.gram,
            caffe=self.caffe
        )
        Product.objects.create(
            name="product4",
            category=self.second,
            unit=self.liter,
            caffe=self.caffe
        )
        product1 = Product.objects.create(
            name="product2",
            category=self.cakes,
            unit=self.liter,
            caffe=self.caffe
        )
        product2 = Product.objects.create(
            name="product3",
            category=self.second,
            unit=self.gram,
            caffe=self.caffe
        )

        self.assertEqual(product1.name, "product2")
        self.assertEqual(product1.caffe, self.caffe)

        self.assertEqual(self.cakes.product_set.count(), 2)
        product1.delete()
        self.assertEqual(self.cakes.product_set.count(), 1)

        product2.category = self.cakes
        product2.save()
        self.assertEqual(self.cakes.product_set.count(), 2)
        self.assertEqual(self.second.product_set.count(), 1)
        product2.category = self.second
        product2.save()

        self.assertEqual(self.gram.product_set.count(), 2)
        product2.delete()
        self.assertEqual(self.gram.product_set.count(), 1)

        # already exists product with name = "product1"
        with self.assertRaises(Exception):
            Product.objects.create(
                name="product1",
                category=self.cakes,
                unit=self.gram,
                caffe=self.caffe
            )

        Product.objects.create(
            name="product1",
            category=self.cakes1,
            unit=self.gram1,
            caffe=self.filtry
        )


class FullProductModelTest(TestCase):
    """FullProduct tests."""

    def setUp(self):
        """Test data setup."""

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
            category=first_cat,
            unit=liter,
            caffe=self.caffe
        )
        Product.objects.create(
            name="product3",
            category=second_cat,
            unit=gram,
            caffe=self.caffe
        )
        Product.objects.create(
            name="product4",
            category=second_cat,
            unit=liter,
            caffe=self.caffe
        )

    def test_full_product(self):
        """Test creating FullProducts."""

        product1 = Product.objects.get(name="product1")
        product2 = Product.objects.get(name="product2")
        product3 = Product.objects.get(name="product3")
        product4 = Product.objects.get(name="product4")

        report1 = Report.objects.create(caffe=self.caffe)
        report2 = Report.objects.create(caffe=self.caffe)

        full_product1 = FullProduct.objects.create(
            product=product1,
            amount=10,
            report=report1,
            caffe=self.caffe
        )
        full_product2 = FullProduct.objects.create(
            product=product2,
            amount=100,
            report=report1,
            caffe=self.caffe
        )
        full_product3 = FullProduct.objects.create(
            product=product4,
            amount=1000,
            report=report2,
            caffe=self.caffe
        )
        FullProduct.objects.create(
            product=product3,
            amount=0,
            report=report2,
            caffe=self.caffe
        )

        self.assertEqual(full_product1.product.name, "product1")
        self.assertEqual(full_product1.caffe, self.caffe)
        self.assertEqual(full_product2.amount, 100)
        self.assertEqual(full_product2.report.id, report1.id)

        self.assertEqual(report2.full_products.count(), 2)
        full_product3.delete()
        self.assertEqual(report2.full_products.count(), 1)

        self.assertEqual(report1.full_products.count(), 2)
        product2.delete()
        self.assertEqual(report1.full_products.count(), 1)

        full_product1.amount = -1


class ReportModelTest(TestCase):
    """Report tests."""

    def setUp(self):
        """Data setup for tests."""

        self.caffe = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        report1 = Report.objects.create(caffe=self.caffe)
        report2 = Report.objects.create(caffe=self.caffe)
        report3 = Report.objects.create(caffe=self.caffe)
        report4 = Report.objects.create(caffe=self.caffe)

        first_cat = Category.objects.create(name="first", caffe=self.caffe)
        second_cat = Category.objects.create(name="second", caffe=self.caffe)

        gram = Unit.objects.create(name="gram", caffe=self.caffe)
        liter = Unit.objects.create(name="liter", caffe=self.caffe)

        product1 = Product.objects.create(
            name="product1",
            category=first_cat,
            unit=gram,
            caffe=self.caffe
        )
        product2 = Product.objects.create(
            name="product2",
            category=first_cat,
            unit=liter,
            caffe=self.caffe
        )
        product3 = Product.objects.create(
            name="product3",
            category=second_cat,
            unit=gram,
            caffe=self.caffe
        )
        product4 = Product.objects.create(
            name="product4",
            category=second_cat,
            unit=liter,
            caffe=self.caffe
        )

        FullProduct.objects.create(
            product=product1,
            amount=10,
            report=report1,
            caffe=self.caffe
        )

        FullProduct.objects.create(
            product=product2,
            amount=100,
            report=report2,
            caffe=self.caffe
        )
        FullProduct.objects.create(
            product=product3,
            amount=0,
            report=report3,
            caffe=self.caffe
        )

        FullProduct.objects.create(
            product=product4,
            amount=1000,
            report=report4,
            caffe=self.caffe
        )

    def test_create(self):
        """Check creating reports."""
        self.assertEqual(Report.objects.count(), 4)

        report = Report.objects.first()
        self.assertEqual(report.caffe, self.caffe)

    def test_doubles(self):
        """Check if two fullproducts with same product are not allowed."""

        report1 = Report.objects.get(id=1)
        product = FullProduct.objects.first().product

        with self.assertRaises(Exception):
            FullProduct.objects.create(
                product=product,
                amount=1,
                report=report1
            )
