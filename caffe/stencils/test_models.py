# -*- encoding: utf-8 -*-

from django.test import TestCase

from .models import Stencil
from reports.models import Category

class StencilModelTest(TestCase):
    """Tests Stencil model."""

    def setUp(self):
        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

    def test_stencil_name(self):
        """Checks if name for Stencil is saved properly."""

        stencil = Stencil.objects.create(name='Poranny')

        get_stencil = Stencil.objects.get(id=stencil.id)
        self.assertEqual(get_stencil.name, 'Poranny')

    def test_stencil_same_name(self):
        """Checks if two Stencils cannot have the same name."""

        stencil = Stencil.objects.create(name='Poranny')
        with self.assertRaises(Exception):
            stencil = Stencil.objects.create(name='Poranny')

    def test_stencil_categories(self):
        """Checks if category/categories for Stencil are saved properly."""

        stencil = Stencil.objects.create(name='Poranny')
        stencil.categories.add(self.caffees, self.cakes)

        get_stencil = Stencil.objects.get(id=stencil.id)
        self.assertListEqual(
            list(get_stencil.categories.all()),
            [self.caffees, self.cakes]
        )
