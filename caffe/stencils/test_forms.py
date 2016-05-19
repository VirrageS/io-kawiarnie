# -*- encoding: utf-8 -*-

from django.test import TestCase

from reports.models import Category

from .forms import StencilForm
from .models import Stencil


class StencilFormTest(TestCase):
    """Tests Stencil form."""

    def setUp(self):
        """Initialize all Categories needed for further tests."""

        self.coffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

    def test_stencil_form_correct(self):
        """Check possible cases when StencilForm is correct."""

        form_correct = StencilForm({
            'name': 'Poranny',
            'description': '',
            'categories': [self.coffees.id]
        })

        self.assertCountEqual(
            [cat for cat in form_correct.fields['categories'].choices],
            [(cat.id, cat.name) for cat in [self.coffees, self.cakes]]
        )
        self.assertTrue(form_correct.is_valid())

        self.assertCountEqual(
            list(form_correct.cleaned_data['categories']),
            [self.coffees]
        )

    def test_stencil_form_incorrect(self):
        """Check possible cases when StencilForm is not correct."""

        form_incorrect = StencilForm({
            'name': '',
            'categories': [self.cakes.id]
        })

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = StencilForm({
            'name': 'Poranny',
            'categories': []
        })

        self.assertFalse(form_incorrect.is_valid())

    def test_stencil_form_instance(self):
        """Check Stencil form with loaded instance."""

        stencil = Stencil.objects.create(name='Poranny')
        stencil.categories.add(self.coffees, self.cakes)

        get_stencil = Stencil.objects.get(id=stencil.id)

        form_correct = StencilForm(
            {
                'name': 'Wieczorny',
                'categories': [self.cakes.id]
            },
            instance=get_stencil
        )
        self.assertIsInstance(form_correct.instance, Stencil)
        self.assertEqual(form_correct.instance.id, get_stencil.id)

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

        get_stencil = Stencil.objects.get(id=stencil.id)
        self.assertEqual(get_stencil.name, 'Wieczorny')
        self.assertListEqual(list(get_stencil.categories.all()), [self.cakes])
