# -*- encoding: utf-8 -*-
# pylint: disable=C0103

from django.test import TestCase

from reports.models import Category

from .models import Stencil


class StencilModelTest(TestCase):
    """Test for Stencil model."""

    def setUp(self):
        """Initialize all categories needed in tests."""

        self.coffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

    def test_stencil_name(self):
        """Check if name for Stencil is saved properly."""

        stencil = Stencil.objects.create(name='Poranny')

        get_stencil = Stencil.objects.get(id=stencil.id)
        self.assertEqual(get_stencil.name, 'Poranny')

    def test_stencil_name_empty(self):
        """Check that the name can't be an empty string."""

        with self.assertRaises(Exception):
            Stencil.objects.create(name='')

    def test_stencil_name_whitespace(self):
        """Check that the name can't consist of whitespace."""

        with self.assertRaises(Exception):
            Stencil.objects.create(name=' ')

        with self.assertRaises(Exception):
            Stencil.objects.create(name='                  ')

    def test_stencil_same_name(self):
        """Check if two Stencils cannot have the same name."""

        Stencil.objects.create(name='Poranny')

        with self.assertRaises(Exception):
            Stencil.objects.create(name='Poranny')

    def test_stencil_same_name_case_insensitive(self):
        """Check that two Stencils can't have the same name."""

        Stencil.objects.create(name='Poranny')

        with self.assertRaises(Exception):
            Stencil.objects.create(name='poranny')

    def test_stencil_description(self):
        """Check if description for Stencil is saved properly."""

        stencil = Stencil.objects.create(
            name='Poranny',
            description=u'Szablon do raportów na sam początek dnia'
        )

        get_stencil = Stencil.objects.get(id=stencil.id)
        self.assertEqual(
            get_stencil.description,
            u'Szablon do raportów na sam początek dnia'
        )

    def test_stencil_categories(self):
        """Check if category/categories for Stencil are saved properly."""

        stencil = Stencil.objects.create(name='Poranny')
        stencil.categories.add(self.coffees, self.cakes)

        get_stencil = Stencil.objects.get(id=stencil.id)
        self.assertListEqual(
            list(get_stencil.categories.all()),
            [self.coffees, self.cakes]
        )

    def test_stencil_same_categories(self):
        """Check that two same categories can't be added."""

        stencil = Stencil.objects.create(name='Wieczorny')
        stencil.categories.add(self.coffees, self.coffees)

        self.assertEqual(len(list(stencil.categories.all())), 1)

    def test_stencil_to_string(self):
        """Check if str() on Stencil returns good value."""

        stencil = Stencil.objects.create(name='Poranny', description='Hello')
        stencil.categories.add(self.coffees, self.cakes)

        self.assertEqual(stencil.name, str(stencil))
