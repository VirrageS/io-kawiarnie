# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

import collections

from stencils.models import Stencil
from reports.models import Category, FullProduct, Report, Product, Unit

from stencils.forms import StencilForm

class StencilViewTests(TestCase):
    """Tests views for Stencil model."""

    def compare_stencils(self, stencil1, stencil2):
        """
        Comapre 2 stencils
            args: stencil1, stencil2
            return: True is stencils are equal
                    False is are not
        """

        if (stencil1.name != stencil2.name
            or stencil1.description != stencil2.description
            or collections.Counter(stencil1.categories.all()) != 
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
        self.liter = Unit.objects.create(name='litr')

        self.coke = Product.objects.create(
            name="Cola",
            category=self.juices,
            unit=self.liter
        )

        self.green_tea = Product.objects.create(
            name="Zielona Herbata",
            category=self.tees,
            unit=self.liter
        )

        self.black_coffe = Product.objects.create(
            name="Czarna kawa",
            category=self.caffees,
            unit=self.liter
        )

        self.to_drink = Stencil.objects.create(
            name='Do picia',
            description='picie'
        )

        self.to_drink.categories.add(self.tees, self.juices)

        self.to_eat = Stencil.objects.create(
            name='Do jedzenia',
            description='jedzenie'
        )
        self.to_eat.categories.add(self.cakes, self.caffees)

    def test_stencil_show_all(self):
        """Check if all stencils view is displayed properly."""

        response = self.client.get(reverse('stencils_show_all_stencils'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/all.html')

        # check context
        self.assertEqual(len(response.context['stencils']), 2)
        stencils = response.context['stencils']
        for stencil in stencils:
            if stencil.name == 'Do picia':
                self.assertTrue(self.compare_stencils(stencil, self.to_drink))
            elif stencil.name == 'Do jedzenia':
                self.assertTrue(self.compare_stencils(stencil, self.to_eat))
            else:
                self.assertTrue(False)

    def test_stencil_show(self):
        """Check if stencil view is displated properly."""
        response = self.client.get(reverse(
            'stencils_show_stencil',
            args=(self.to_drink.id,)
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/show.html')

        stencil = response.context['stencil']
        categories = response.context['categories']

        self.assertTrue(self.compare_stencils(stencil, self.to_drink))
        self.assertEqual(
            collections.Counter(categories),
            collections.Counter(self.to_drink.categories.all())
        )

    def test_edit_stencil_show(self):
        """Check if edit category view is displayed properly."""

        response = self.client.get(
            reverse('stencils_edit_stencil', args=(self.to_drink.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/edit_stencil.html')

        form = response.context['form']
        self.assertIsInstance(form, StencilForm)
        self.assertEqual(form.instance, self.to_drink)

        self.assertEqual(len(response.context), 2)

    def test_edit_stencil_post_success(self):
        """Check success of edit stencil post request."""

        form = {}
        form['name'] = u'Moj szablon'
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [self.cakes.id, self.tees.id]

        st_form = StencilForm(form)
        self.assertTrue(st_form.is_valid())

        response = self.client.post(
            reverse('stencils_edit_stencil', args=(self.to_drink.id,)),
            form
        )

        self.assertEqual(Stencil.objects.count(), 2)
        self.assertEqual(response.status_code, 302)

    def test_edit_stencil_post_failure(self):
        """Check failure of edit stencil post request."""

        form = {}
        form['name'] = u''
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [self.cakes.id, self.tees.id]

        st_form = StencilForm(form)
        self.assertFalse(st_form.is_valid())

        response = self.client.post(
            reverse('stencils_edit_stencil', args=(self.to_drink.id,)),
            form
        )

        self.assertEqual(Stencil.objects.count(), 2)
        self.assertEqual(response.status_code, 200)

        form['name'] = u'Nazwa'
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [-10, self.tees.id]

        st_form = StencilForm(form)
        self.assertFalse(st_form.is_valid())

        response = self.client.post(
            reverse('stencils_edit_stencil', args=(self.to_eat.id,)),
            form
        )

        self.assertEqual(Stencil.objects.count(), 2)
        self.assertEqual(response.status_code, 200)


    def test_new_stencil(self):
        """Check form to create new stencil."""

        response = self.client.get(reverse('stencils_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/create_stencil.html')
        self.assertEqual(Stencil.objects.count(), 2)

    def test_new_stencil_post_success(self):
        """Check success of new stencil post request."""

        form = {}
        form['name'] = u'Moj szablon'
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [self.cakes.id, self.tees.id]

        st_form = StencilForm(form)
        self.assertTrue(st_form.is_valid())

        response = self.client.post(
            reverse('stencils_new_stencil'),
            form
        )

        self.assertEqual(Stencil.objects.count(), 3)
        self.assertEqual(response.status_code, 302)

    def test_new_stencil_post_failure(self):
        """Check failure of new stencil post request."""

        form = {}
        form['name'] = u''
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [self.cakes.id, self.tees.id]

        st_form = StencilForm(form)
        self.assertFalse(st_form.is_valid())

        response = self.client.post(
            reverse('stencils_new_stencil'),
            form
        )

        self.assertEqual(Stencil.objects.count(), 2)
        self.assertEqual(response.status_code, 200)

        form['name'] = u'Nazwa'
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [-10, self.tees.id]

        st_form = StencilForm(form)
        self.assertFalse(st_form.is_valid())

        response = self.client.post(
            reverse('stencils_create'),
            form
        )

        self.assertEqual(Stencil.objects.count(), 2)
        self.assertEqual(response.status_code, 200)

    # this view is not used anywhere
    '''
    def test_edit_stencil_report(self):
        """Check rendering edit report form."""

        full_product = FullProduct.objects.create(
            product=self.black_coffe,
            amount=10
        )

        report = Report.objects.create()

        report.save()
        full_product.report = report
        full_product.save()

        response = self.client.get(
            reverse('stencils_edit_report', args=(report.id,))
        )
    '''   

    def test_new_stencil_report(self):
        """Check rendering new stencil report page."""

        response = self.client.get(
            reverse('stencils_new_report', args=(self.to_drink.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/new_report.html')

        stencil = response.context['stencil']
        self.assertTrue(self.compare_stencils(stencil, self.to_drink))

        with self.assertRaises(NoReverseMatch):
            self.client.get(
                reverse('stencils_new_report', args=(-1,))
            )

    def test_stencil_report_post_success(self):
        """Check success of creating new report from stencil."""

        post = {}
        post[self.coke.id] = [self.coke.id, 10]
        post[self.green_tea.id] = [self.green_tea.id, 20]
        post['csrfmiddlewaretoken'] = 'hasz hasz hasz ####'


        response = self.client.post(
            reverse('stencils_new_report',
            args=(self.to_drink.id,)),
            post
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.count(), 1)

    def test_stencil_report_post_fail(self):
        """Check failure of creating new report from stencil."""

        # wrong amount, should render the same page (200)
        post = {}
        post[self.coke.id] = [self.coke.id, -20]
        post[self.green_tea.id] = [self.green_tea.id, 20]

        response = self.client.post(
            reverse('stencils_new_report',
            args=(self.to_drink.id,)),
            post
        )

        self.assertEqual(response.status_code, 200)

        # report should not pass with no products
        post = {}

        response = self.client.post(
            reverse('stencils_new_report',
            args=(self.to_drink.id,)),
            post
        )

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(NoReverseMatch):
            self.client.post(
                reverse('stencils_new_report',
                args=(-1,)),
                post
            )

