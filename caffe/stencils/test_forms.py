# -*- encoding: utf-8 -*-

from django.test import TestCase

from caffe.models import Caffe
from reports.models import Category

from .forms import StencilForm
from .models import Stencil


class StencilFormTest(TestCase):
    """Tests Stencil form."""

    def setUp(self):
        """Initialize all Categories needed for further tests."""

        self.kafo = Caffe.objects.create(
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

        self.coffees = Category.objects.create(name='Kawy', caffe=self.kafo)
        self.cakes = Category.objects.create(name='Ciasta', caffe=self.kafo)
        self.cakes_f = Category.objects.create(
            name='Ciasta',
            caffe=self.filtry
        )

    def test_stencil_form_correct(self):
        """Check possible cases when StencilForm is correct."""

        form_correct = StencilForm(
            {
                'name': 'Poranny',
                'description': '',
                'categories': [self.coffees.id]
            },
            caffe=self.kafo
        )

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

        form_incorrect = StencilForm(
            {'name': '', 'categories': [self.cakes.id]},
            caffe=self.kafo
        )

        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = StencilForm(
            {
                'name': 'Poranny',
                'categories': []
            },
            caffe=self.kafo
        )

        self.assertFalse(form_incorrect.is_valid())

    def test_stencil_same_name(self):
        """Check if Stencil with same name cannot be created."""

        Stencil.objects.create(name='Poranny', caffe=self.kafo)
        form_incorrect = StencilForm(
            {'name': 'Poranny', 'categories': [self.cakes.id]},
            caffe=self.kafo
        )
        self.assertFalse(form_incorrect.is_valid())

        form_correct = StencilForm(
            {'name': 'Poranny', 'categories': [self.cakes_f.id]},
            caffe=self.filtry
        )
        self.assertTrue(form_correct.is_valid())

    def test_stencil_categories(self):
        """Check if Stencil categories are properly cleaned."""

        form_incorrect = StencilForm(
            {'name': 'Poranny', 'categories': [self.cakes_f.id]},
            caffe=self.kafo
        )
        self.assertFalse(form_incorrect.is_valid())

        form_incorrect = StencilForm(
            {'name': 'Por', 'categories': [self.cakes.id, self.cakes_f.id]},
            caffe=self.kafo
        )
        self.assertFalse(form_incorrect.is_valid())

    def test_stencil_form_instance(self):
        """Check Stencil form with loaded instance."""

        stencil = Stencil.objects.create(name='Poranny', caffe=self.kafo)
        stencil.categories.add(self.coffees, self.cakes)

        get_stencil = Stencil.objects.get(id=stencil.id)

        form_correct = StencilForm(
            {'name': 'Wieczorny', 'categories': [self.cakes.id]},
            instance=get_stencil,
            caffe=self.kafo
        )

        self.assertIsInstance(form_correct.instance, Stencil)
        self.assertEqual(form_correct.instance.id, get_stencil.id)

        self.assertTrue(form_correct.is_valid())
        form_correct.save()

        get_stencil = Stencil.objects.get(id=stencil.id)
        self.assertEqual(get_stencil.name, 'Wieczorny')
        self.assertListEqual(list(get_stencil.categories.all()), [self.cakes])
