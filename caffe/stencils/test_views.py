# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

import collections

from stencils.models import Stencil
from reports.models import Category

from stencils.forms import StencilForm

class StencilViewTests(TestCase):
    """Tests views for Stencil model."""

    def compareStencils(self, stencil1, stencil2):
        """Comapre 2 stencils
            args: stencil1, stencil2
            return: True is stencils are equal
                    False is are not
        """

        if (stencil1.name != stencil2.name or 
            stencil1.description != stencil2.description or
            collections.Counter(stencil1.categories.all()) != 
            collections.Counter(stencil2.categories.all())):
            return False

        return True

    def setUp(self):
        """test data setup."""
        self.client = Client()

        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')
        self.tees = Category.objects.create(name='Herbaty')
        self.juices = Category.objects.create(name='Soki')

        self.toDrink = Stencil.objects.create(
            name='Do picia',
            description='picie'
        )

        self.toDrink.categories.add(self.tees, self.juices) 
    

        self.toEat = Stencil.objects.create(
            name='Do jedzenia',
            description='jedzenie'
        )
        self.toEat.categories.add(self.cakes, self.caffees)

    def test_stencil_show_all(self):
        """Check if all stencils view is displayed properly."""

        response = self.client.get(reverse('stencils_show_all_stencils'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/all.html')

        # check context
        self.assertEqual(len(response.context['stencils']), 2)
        stencils = response.context['stencils']
        for stencil in stencils:
            if stencil.name=='Do picia':
                self.assertTrue(self.compareStencils(stencil, self.toDrink))
            elif stencil.name=='Do jedzenia':
                self.assertTrue(self.compareStencils(stencil, self.toEat))
            else:
                self.assertTrue(False)

    def test_stencil_show(self):
        """Check if stencil view is displated properly."""
        response = self.client.get(reverse(
            'stencils_show_stencil',
            args=(self.toDrink.id,)
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/show.html')

        stencil = response.context['stencil']
        categories = response.context['categories']

        self.assertTrue(self.compareStencils(stencil, self.toDrink))
        self.assertEqual(
            collections.Counter(categories),
            collections.Counter(self.toDrink.categories.all())
        )

    def test_edit_stencil_show(self):
        """Check if edit category view is displayed properly."""

        response = self.client.get(
            reverse('stencils_edit_stencil', args=(self.toDrink.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/edit_stencil.html')

        form = response.context['form']
        self.assertIsInstance(form, StencilForm)
        self.assertEqual(form.instance, self.toDrink)

        self.assertEqual(len(response.context), 2)
        
    def test_new_stencil(self):
        """Check form to create new stencil."""

        response = self.client.get(reverse('stencils_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/create_stencil.html')

    def test_new_stencil_report(self):

        response = self.client.get(
            reverse('stencils_new_report', args=(self.toDrink.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/new_report.html')

        stencil = response.context['stencil']
        self.assertTrue(self.compareStencils(stencil, self.toDrink))
