"""Reports models tests module."""
# -*- encoding: utf-8 -*-

from django.test import TestCase

from .models import Category, FullProduct, Product, Report, Unit


class CategoryModelTest(TestCase):
    """Category tests."""

    def setUp(self):
        """Test data setup."""
        Category.objects.create(name="first")
        Category.objects.create(name="second")

    def test_category_name(self):
        """Chcek correctness of setting names."""
        category1 = Category(name="first")
        category2 = Category(name="second")

        self.assertTrue(category1.name != category2.name)
        self.assertEqual(category1.name, "first")
        self.assertEqual(category2.name, "second")
        self.assertRaises(Exception, Category.objects.create, name="first")
        self.assertRaises(Exception, Category.objects.create, name="second")


class UnitModelTest(TestCase):
    """Unit tests."""

    def setUp(self):
        """Test data setup."""
        Unit.objects.create(name="gram")
        Unit.objects.create(name="liter")

    def test_unit(self):
        """Chcek creating units."""
        u_gram = Unit.objects.get(name="gram")
        u_gram2 = Unit.objects.get(name="gram")
        Unit.objects.get(name="liter")

        self.assertEqual(u_gram.id, u_gram2.id)
        self.assertRaises(Exception, Unit.objects.create, name="liter")


class ProductModelTest(TestCase):
    """Product tests."""

    def setUp(self):
        """Test data setup."""
        Category.objects.create(name="first")
        Category.objects.create(name="second")

        Unit.objects.create(name="gram")
        Unit.objects.create(name="liter")

    def test_product(self):
        """Check correctness of creating products and validation."""
        first_cat = Category.objects.get(name="first")
        second_cat = Category.objects.get(name="second")

        gram = Unit.objects.get(name="gram")
        liter = Unit.objects.get(name="liter")

        Product.objects.create(
            name="product1",
            category=first_cat,
            unit=gram
        )
        Product.objects.create(
            name="product4",
            category=second_cat,
            unit=liter
        )
        product1 = Product.objects.create(
            name="product2",
            category=first_cat,
            unit=liter
        )
        product2 = Product.objects.create(
            name="product3",
            category=second_cat,
            unit=gram
        )
        self.assertEqual(first_cat.product_set.count(), 2)
        product1.delete()
        self.assertEqual(first_cat.product_set.count(), 1)
        product2.category = first_cat
        product2.save()
        self.assertEqual(first_cat.product_set.count(), 2)
        self.assertEqual(second_cat.product_set.count(), 1)
        product2.category = second_cat
        product2.save()

        self.assertEqual(gram.product_set.count(), 2)
        product2.delete()
        self.assertEqual(gram.product_set.count(), 1)

        # already exists product with name = "product1"
        self.assertRaises(
            Exception,
            Product.objects.create,
            name="product1",
            category=first_cat,
            unit=gram
        )


class FullProductModelTest(TestCase):
    """FullProduct tests."""

    def setUp(self):
        """Test data setup."""
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

    def test_full_product(self):
        """Test creating FullProducts."""
        product1 = Product.objects.get(name="product1")
        product2 = Product.objects.get(name="product2")
        product3 = Product.objects.get(name="product3")
        product4 = Product.objects.get(name="product4")

        report1 = Report.objects.create(id=1)
        report2 = Report.objects.create(id=2)

        full_product1 = FullProduct.objects.create(
            product=product1,
            amount=10,
            report=report1
        )
        full_product2 = FullProduct.objects.create(
            product=product2,
            amount=100,
            report=report1
        )
        full_product3 = FullProduct.objects.create(
            product=product4,
            amount=1000,
            report=report2
        )
        FullProduct.objects.create(
            product=product3,
            amount=0,
            report=report2
        )

        self.assertEqual(full_product1.product.name, "product1")
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
        report1 = Report.objects.create(id=1)
        report2 = Report.objects.create(id=2)
        report3 = Report.objects.create(id=3)
        report4 = Report.objects.create(id=4)

        first_cat = Category.objects.create(name="first")
        second_cat = Category.objects.create(name="second")

        gram = Unit.objects.create(name="gram")
        liter = Unit.objects.create(name="liter")

        product1 = Product.objects.create(
            name="product1",
            category=first_cat,
            unit=gram
        )
        product2 = Product.objects.create(
            name="product2",
            category=first_cat,
            unit=liter
        )
        product3 = Product.objects.create(
            name="product3",
            category=second_cat,
            unit=gram
        )
        product4 = Product.objects.create(
            name="product4",
            category=second_cat,
            unit=liter
        )

        FullProduct.objects.create(
            product=product1,
            amount=10,
            report=report1
        )

        FullProduct.objects.create(
            product=product2,
            amount=100,
            report=report2
        )
        FullProduct.objects.create(
            product=product3,
            amount=0,
            report=report3
        )

        FullProduct.objects.create(
            product=product4,
            amount=1000,
            report=report4
        )

    def test_create(self):
        """Check creating reports."""
        self.assertEqual(Report.objects.count(), 4)

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
