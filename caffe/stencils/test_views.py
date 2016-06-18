# -*- encoding: utf-8 -*-
# pylint: disable=C0103,R0902

import collections

from django.contrib.auth.models import Permission
from django.core.urlresolvers import NoReverseMatch, reverse
from django.test import Client, TestCase, RequestFactory

from caffe.models import Caffe
from employees.models import Employee
from reports.models import Category, Product, Report, Unit

from .forms import StencilForm
from .models import Stencil
from .views import stencils_new_stencil, stencils_edit_stencil


class StencilViewTests(TestCase):
    """Tests views for Stencil model."""

    @classmethod
    def compare_stencils(cls, stencil1, stencil2):
        """Comapre 2 stencils.

        Args: stencil1, stencil2
        Return: True if stencils are equal, False otherwise
        """

        cat1 = stencil1.categories.all()
        cat2 = stencil2.categories.all()

        if (stencil1.name != stencil2.name or
                stencil1.description != stencil2.description or
                collections.Counter(cat1) != collections.Counter(cat2)):
            return False

        return True

    def setUp(self):
        """test data setup."""
        self.client = Client()

        self.kafo = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        self.caffees = Category.objects.create(name='Kawy', caffe=self.kafo)
        self.cakes = Category.objects.create(name='Ciasta', caffe=self.kafo)
        self.tees = Category.objects.create(name='Herbaty', caffe=self.kafo)
        self.juices = Category.objects.create(name='Soki', caffe=self.kafo)
        self.liter = Unit.objects.create(name='litr', caffe=self.kafo)

        self.coke = Product.objects.create(
            name="Cola",
            category=self.juices,
            unit=self.liter,
            caffe=self.kafo
        )

        self.green_tea = Product.objects.create(
            name="Zielona Herbata",
            category=self.tees,
            unit=self.liter,
            caffe=self.kafo
        )

        self.black_coffe = Product.objects.create(
            name="Czarna kawa",
            category=self.caffees,
            unit=self.liter,
            caffe=self.kafo
        )

        self.to_drink = Stencil.objects.create(
            name='Do picia',
            description='picie',
            caffe=self.kafo
        )

        self.to_drink.categories.add(self.tees, self.juices)

        self.to_eat = Stencil.objects.create(
            name='Do jedzenia',
            description='jedzenie',
            caffe=self.kafo
        )
        self.to_eat.categories.add(self.cakes, self.caffees)

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin',
            caffe=self.kafo
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_stencil'),
            Permission.objects.get(codename='change_stencil'),
            Permission.objects.get(codename='view_stencil'),
            Permission.objects.get(codename='add_report'),
        )

        self.client.login(username='admin', password='admin')

        self.factory = RequestFactory()

    def test_stencil_show_all(self):
        """Check if all stencils view is displayed properly."""

        response = self.client.get(reverse('stencils_show_all_stencils'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stencils/all.html')

        # check context
        self.assertEqual(len(response.context['stencils']), 2)
        stencils = list(response.context['stencils'])
        self.assertListEqual(
            stencils,
            sorted(stencils, key=lambda stencil: stencil.name, reverse=False)
        )

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

    def test_edit_stencil_post_success(self):
        """Check success of edit stencil post request."""

        form = {}
        form['name'] = u'Moj szablon'
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [self.cakes.id, self.tees.id]

        st_form = StencilForm(form, caffe=self.kafo)
        self.assertTrue(st_form.is_valid())

        request = self.factory.post(
            reverse('stencils_edit_stencil', args=(self.to_drink.id,)),
            form)
        request.user = self.user
        response = stencils_edit_stencil(request, self.to_drink.id)

        edited_stencil = Stencil.objects.get(id=self.to_drink.id)

        self.assertCountEqual(Stencil.objects.all(),
                              [self.to_eat, edited_stencil])
        self.assertEqual(response.status_code, 302)

    def test_edit_stencil_post_failure(self):
        """Check failure of edit stencil post request."""

        form = {}
        form['name'] = u''
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [self.cakes.id, self.tees.id]

        st_form = StencilForm(form, caffe=self.kafo)
        self.assertFalse(st_form.is_valid())

        request = self.factory.post(
            reverse('stencils_edit_stencil', args=(self.to_drink.id,)),
            form,)
        request.user = self.user
        response = stencils_edit_stencil(request, self.to_drink.id)

        self.assertCountEqual(Stencil.objects.all(),
                              [self.to_drink, self.to_eat])
        self.assertEqual(response.status_code, 200)

        form['name'] = u'Nazwa'
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [-10, self.tees.id]

        st_form = StencilForm(form, caffe=self.kafo)
        self.assertFalse(st_form.is_valid())

        request = self.factory.post(
            reverse('stencils_edit_stencil', args=(self.to_drink.id,)),
            form)
        request.user = self.user
        response = stencils_edit_stencil(request, self.to_drink.id)

        self.assertCountEqual(Stencil.objects.all(),
                              [self.to_drink, self.to_eat])
        self.assertEqual(response.status_code, 200)

    def test_new_stencil_post_success(self):
        """Check success of new stencil post request."""

        form = {}
        form['name'] = u'Moj szablon'
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [self.cakes.id, self.tees.id]

        self.assertEqual(self.user.caffe, self.kafo)
        st_form = StencilForm(form, caffe=self.user.caffe)
        self.assertTrue(st_form.is_valid())

        request = self.factory.post(reverse('stencils_new_stencil'), form)
        request.user = self.user
        response = stencils_new_stencil(request)

        new_stencil = Stencil.objects.get(name='Moj szablon')

        self.assertCountEqual(Stencil.objects.all(),
                              [self.to_drink, self.to_eat, new_stencil])
        self.assertEqual(response.status_code, 302)

    def test_new_stencil_post_failure(self):
        """Check failure of new stencil post request."""

        form = {}
        form['name'] = u''
        form['description'] = u'Opis mojego szablonu'
        form['categories'] = [self.cakes.id, self.tees.id]

        st_form = StencilForm(form, caffe=self.kafo)
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

        st_form = StencilForm(form, caffe=self.kafo)
        self.assertFalse(st_form.is_valid())

        request = self.factory.post(reverse('stencils_new_stencil'), form)
        request.user = self.user
        response = stencils_new_stencil(request)

        self.assertCountEqual(Stencil.objects.all(),
                              [self.to_drink, self.to_eat])
        self.assertEqual(response.status_code, 200)

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
            reverse('stencils_new_report', args=(self.to_drink.id,)),
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
            reverse('stencils_new_report', args=(self.to_drink.id,)),
            post
        )

        self.assertEqual(response.status_code, 200)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("niepoprawnie" in messages[0].message)

        # report should not pass with no products
        post = {}

        response = self.client.post(
            reverse('stencils_new_report', args=(self.to_drink.id,)),
            post
        )

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(NoReverseMatch):
            self.client.post(
                reverse('stencils_new_report', args=(-1,)),
                post
            )
