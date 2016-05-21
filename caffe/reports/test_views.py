# -*- encoding: utf-8 -*-
# pylint: disable=C0103,R0902,C0302

import json

from django.contrib.auth.models import Permission
from django.core.urlresolvers import NoReverseMatch, reverse
from django.test import Client, TestCase
from django.utils import timezone

from employees.models import Employee
from .forms import CategoryForm, ProductForm, UnitForm
from .models import Category, FullProduct, Product, Report, Unit
from .views import get_report_categories


class CategoryViewsTests(TestCase):
    """Test all views of the Category model."""

    def setUp(self):
        """Initialize all categories needed in tests."""

        self.client = Client()

        self.coffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_category'),
            Permission.objects.get(codename='change_category'),
            Permission.objects.get(codename='view_report'),
        )

        self.client.login(username='admin', password='admin')

    def test_new_category_show(self):
        """Check if new category view is displayed properly."""

        response = self.client.get(reverse('reports_new_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], CategoryForm)
        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            'Nowa kategoria'
        )

        elements = response.context['elements']
        self.assertEqual(len(elements), 2)
        self.assertListEqual(
            elements,
            sorted(elements, key=lambda x: x['desc'], reverse=False)
        )

        for element in elements:
            self.assertEqual(len(element), 3)
            self.assertIn(
                element['edit_href'], [
                    reverse('reports_edit_category', args=(self.coffees.id,)),
                    reverse('reports_edit_category', args=(self.cakes.id,))
                ]
            )
            self.assertIn(element['id'], [self.coffees.id, self.cakes.id])
            self.assertIn(
                element['desc'],
                [str(self.coffees), str(self.cakes)]
            )

    def test_new_category_post_fail(self):
        """Check if new category fails to create when form is not valid."""

        response = self.client.post(
            reverse('reports_new_category'),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'reports/new_element.html')

    def test_new_category_post_success(self):
        """Check if new category successes to create when form is valid."""

        response = self.client.post(
            reverse('reports_new_category'),
            {u'name': u'Napoje'},
            follow=True
        )

        self.assertRedirects(response, reverse('reports_navigate'))

        # check if new category is displayed
        response = self.client.get(reverse('reports_new_category'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)
        self.assertListEqual(
            response.context['elements'],
            sorted(
                response.context['elements'],
                key=lambda x: x['desc'],
                reverse=False
            )
        )

        new_category = Category.objects.get(name='Napoje')
        self.assertIsNotNone(new_category)
        self.assertIsInstance(new_category, Category)

    def test_edit_category_show(self):
        """Check if edit category view is displayed properly."""

        response = self.client.get(
            reverse('reports_edit_category', args=(self.coffees.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, CategoryForm)
        self.assertEqual(form.instance, self.coffees)

        self.assertEqual(len(response.context['context']), 2)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj kategorię'
        )
        self.assertEqual(
            response.context['context']['cancel_href'],
            reverse('reports_new_category')
        )

    def test_edit_category_404(self):
        """Check if 404 is displayed when category does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('reports_edit_category', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('reports_edit_category', args=(_id,))

    def test_edit_category_post_fail(self):
        """Check if edit category fails to edit when form is not valid."""

        response = self.client.post(
            reverse('reports_edit_category', args=(self.cakes.id,)),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'reports/edit_element.html')

    def test_edit_category_post_success(self):
        """Check if edit category successes to edit when form is valid."""

        response = self.client.post(
            reverse('reports_edit_category', args=(self.cakes.id,)),
            {u'name': u'Napoje'},
            follow=True
        )

        self.assertRedirects(response, reverse('reports_navigate'))

        # check if category coffees has changed
        category = Category.objects.get(id=self.cakes.id)
        self.assertEqual(category.name, u'Napoje')

        # check if edited category is displayed
        response = self.client.get(reverse('reports_new_category'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class UnitViewsTests(TestCase):
    """Test all views of the Unit model."""

    def setUp(self):
        """Initialize all units needed in tests."""

        self.client = Client()

        self.money = Unit.objects.create(name=u'złotówki')
        self.grams = Unit.objects.create(name=u'gramy')

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_unit'),
            Permission.objects.get(codename='change_unit'),
            Permission.objects.get(codename='view_report'),
        )

        self.client.login(username='admin', password='admin')

    def test_new_unit_show(self):
        """Check if new unit view is displayed properly."""

        response = self.client.get(reverse('reports_new_unit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], UnitForm)
        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            'Nowa jednostka'
        )

        elements = response.context['elements']
        self.assertEqual(len(elements), 2)
        self.assertListEqual(
            elements,
            sorted(elements, key=lambda x: x['desc'], reverse=False)
        )

        for element in elements:
            self.assertEqual(len(element), 3)
            self.assertIn(
                element['edit_href'], [
                    reverse('reports_edit_unit', args=(self.money.id,)),
                    reverse('reports_edit_unit', args=(self.grams.id,))
                ]
            )
            self.assertIn(element['id'], [self.money.id, self.grams.id])
            self.assertIn(element['desc'], [str(self.money), str(self.grams)])

    def test_new_unit_post_fail(self):
        """Check if new unit fails to create when form is not valid."""

        response = self.client.post(
            reverse('reports_new_unit'),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'reports/new_element.html')

    def test_new_unit_post_success(self):
        """Check if new unit successes to create if form is valid."""

        response = self.client.post(
            reverse('reports_new_unit'),
            {u'name': u'sztuki'},
            follow=True
        )

        self.assertRedirects(response, reverse('reports_navigate'))

        # check if new unit is displayed
        response = self.client.get(reverse('reports_new_unit'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)
        self.assertListEqual(
            response.context['elements'],
            sorted(
                response.context['elements'],
                key=lambda x: x['desc'],
                reverse=False
            )
        )

        new_unit = Unit.objects.get(name='sztuki')
        self.assertIsNotNone(new_unit)
        self.assertIsInstance(new_unit, Unit)

    def test_edit_unit_show(self):
        """Check if edit unit view is displayed properly."""

        response = self.client.get(
            reverse('reports_edit_unit', args=(self.money.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, UnitForm)
        self.assertEqual(form.instance, self.money)

        self.assertEqual(len(response.context['context']), 2)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj jednostkę'
        )
        self.assertEqual(
            response.context['context']['cancel_href'],
            reverse('reports_new_unit')
        )

    def test_edit_unit_404(self):
        """Check if 404 is displayed when unit does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('reports_edit_unit', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('reports_edit_unit', args=(_id,))

    def test_edit_unit_post_fail(self):
        """Check if edit unit fails to edit when form is not valid."""

        response = self.client.post(
            reverse('reports_edit_unit', args=(self.grams.id,)),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'reports/edit_element.html')

    def test_edit_unit_post_success(self):
        """Check if edit unit successes to edit when form is valid."""

        response = self.client.post(
            reverse('reports_edit_unit', args=(self.grams.id,)),
            {u'name': u'sztuki'},
            follow=True
        )

        self.assertRedirects(response, reverse('reports_navigate'))

        # check if unit coffees has changed
        unit = Unit.objects.get(id=self.grams.id)
        self.assertEqual(unit.name, u'sztuki')

        # check if edited unit is displayed
        response = self.client.get(reverse('reports_new_unit'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class ProductViewsTests(TestCase):
    """Test all views of the Product model."""

    def setUp(self):
        """Initialize all elements needed in tests."""

        self.client = Client()

        self.grams = Unit.objects.create(name=u'gramy')
        self.pieces = Unit.objects.create(name=u'sztuki')

        self.coffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

        self.caffee = Product.objects.create(
            name='Kawa sypana',
            category=self.coffees,
            unit=self.grams
        )
        self.cake = Product.objects.create(
            name='Szarlotka',
            category=self.cakes,
            unit=self.pieces
        )

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_product'),
            Permission.objects.get(codename='change_product'),
            Permission.objects.get(codename='view_report'),
        )

        self.client.login(username='admin', password='admin')

    def test_new_product_show(self):
        """Check if new product view is displayed properly."""

        response = self.client.get(reverse('reports_new_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], ProductForm)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(response.context['context']['title'], 'Nowy produkt')

        elements = response.context['elements']
        self.assertEqual(len(elements), 2)
        self.assertListEqual(
            elements,
            sorted(elements, key=lambda x: x['desc'], reverse=False)
        )

        for element in elements:
            self.assertEqual(len(element), 3)
            self.assertIn(
                element['edit_href'], [
                    reverse('reports_edit_product', args=(self.caffee.id,)),
                    reverse('reports_edit_product', args=(self.cake.id,))
                ]
            )
            self.assertIn(element['id'], [self.caffee.id, self.cake.id])
            self.assertIn(element['desc'], [str(self.caffee), str(self.cake)])

    def test_new_product_post_fail(self):
        """Check if new product fails to create when form is not valid."""

        response = self.client.post(
            reverse('reports_new_product'),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
            'unit': ['To pole jest wymagane.'],
            'category': ['To pole jest wymagane.']
        })
        self.assertTemplateUsed(response, 'reports/new_element.html')

    def test_new_product_post_success(self):
        """Check if new product successes to create when form is valid."""

        response = self.client.post(
            reverse('reports_new_product'), {
                'name': u'Sernik',
                'category': self.cakes.id,
                'unit': self.pieces.id
            },
            follow=True
        )

        self.assertRedirects(response, reverse('reports_navigate'))

        # check if new product is displayed
        response = self.client.get(reverse('reports_new_product'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)
        self.assertListEqual(
            response.context['elements'],
            sorted(
                response.context['elements'],
                key=lambda x: x['desc'],
                reverse=False
            )
        )

        new_product = Product.objects.get(name=u'Sernik')
        self.assertIsNotNone(new_product)
        self.assertIsInstance(new_product, Product)
        self.assertEqual(new_product.category, self.cakes)
        self.assertEqual(new_product.unit, self.pieces)

    def test_edit_product_show(self):
        """Check if edit product view is displayed properly."""

        response = self.client.get(
            reverse('reports_edit_product', args=(self.caffee.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, ProductForm)
        self.assertEqual(form.instance, self.caffee)

        self.assertEqual(len(response.context['context']), 2)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj produkt'
        )
        self.assertEqual(
            response.context['context']['cancel_href'],
            reverse('reports_new_product')
        )

    def test_edit_product_404(self):
        """Check if 404 is displayed when product does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('reports_edit_product', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('reports_edit_product', args=(_id,))

    def test_edit_product_post_fail(self):
        """Check if edit product fails to edit when form is not valid."""

        response = self.client.post(
            reverse('reports_edit_product', args=(self.cake.id,)),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['To pole jest wymagane.'],
            'unit': ['To pole jest wymagane.'],
            'category': ['To pole jest wymagane.']
        })
        self.assertTemplateUsed(response, 'reports/edit_element.html')

    def test_edit_product_post_success(self):
        """Check if edit product successes to edit when form is valid."""

        response = self.client.post(
            reverse('reports_edit_product', args=(self.cake.id,)), {
                'name': u'Keks',
                'category': self.cakes.id,
                'unit': self.pieces.id
            },
            follow=True
        )

        self.assertRedirects(response, reverse('reports_navigate'))

        # check if product coffees has changed
        product = Product.objects.get(id=self.cake.id)
        self.assertEqual(product.name, u'Keks')
        self.assertEqual(product.category, self.cakes)
        self.assertEqual(product.unit, self.pieces)

        # check if edited product is displayed
        response = self.client.get(reverse('reports_new_product'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class ReportViewsTests(TestCase):
    """Test all views of the Report model."""

    def setUp(self):
        """Initialize all elements needed in tests."""

        self.client = Client()

        self.coffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')
        self.tees = Category.objects.create(name='Herbaty')
        self.juices = Category.objects.create(name='Soki')
        self.liter = Unit.objects.create(name='litr')
        self.pieces = Unit.objects.create(name='kawałki')

        self.coke = Product.objects.create(
            name="Cola",
            category=self.juices,
            unit=self.liter
        )

        self.cake = Product.objects.create(
            name="Tiramisu",
            category=self.cakes,
            unit=self.pieces
        )

        self.cake_second = Product.objects.create(
            name="Szarlotka",
            category=self.cakes,
            unit=self.pieces
        )

        self.green_tea = Product.objects.create(
            name="Zielona Herbata",
            category=self.tees,
            unit=self.liter
        )

        self.black_coffe = Product.objects.create(
            name="Czarna kawa",
            category=self.coffees,
            unit=self.liter
        )

        self.coke_full = FullProduct.objects.create(
            product=self.coke,
            amount=50
        )
        self.coffee_full = FullProduct.objects.create(
            product=self.black_coffe,
            amount=40
        )
        self.cake_full = FullProduct.objects.create(
            product=self.cake,
            amount=10
        )
        self.cake_full_second = FullProduct.objects.create(
            product=self.cake_second,
            amount=50
        )

        self.minor_report = Report.objects.create()
        self.major_report = Report.objects.create()

        self.coffee_full.report = self.minor_report
        self.coffee_full.save()

        self.cake_full_second.report = self.major_report
        self.cake_full.report = self.major_report
        self.cake_full_second.save()
        self.cake_full.save()

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_report'),
            Permission.objects.get(codename='change_report'),
            Permission.objects.get(codename='view_report'),
        )

        self.client.login(username='admin', password='admin')

        self.major_report.creator = self.user
        self.major_report.save()

    def test_new_report_show(self):
        """Check if new report view is displayed properly."""

        response = self.client.get(reverse('reports_new_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_report.html')

        # check context
        reports = list(response.context['reports'])
        self.assertEqual(len(reports), 2)
        self.assertListEqual(
            reports,
            sorted(reports, key=lambda report: report.created_on, reverse=True)
        )

        self.assertEqual(response.context['title'], 'Nowy raport')

        products = response.context['products']
        all_products = Product.objects.all()
        for product in all_products:
            self.assertIn(str(product.id), products)
            self.assertIn(json.dumps(product.name), products)
            self.assertIn(json.dumps(product.unit.name), products)
            self.assertIn(json.dumps(product.category.id), products)
            self.assertIn(json.dumps(product.category.name), products)

    def test_new_report_post_fail(self):
        """Check if new report fails to create when form is not valid."""

        post = {}
        post[self.coke.id] = [self.coke.id, '']
        post[self.green_tea.id] = [self.green_tea.id, 20]
        post['csrfmiddlewaretoken'] = 'hasz hasz hasz ####'

        response = self.client.post(
            reverse('reports_new_report'),
            post,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_report.html')
        self.assertIn('"errors": ["', response.context['products'])
        self.assertIn('To pole jest wymagane.', response.context['products'])

    def test_new_report_post_success(self):
        """Check if new report successes to create."""

        post = {}
        post[self.coke.id] = [self.coke.id, 10]
        post[self.green_tea.id] = [self.green_tea.id, 20]
        post['csrfmiddlewaretoken'] = 'hasz hasz hasz ####'

        response = self.client.post(
            reverse('reports_new_report'),
            post,
            follow=True
        )

        self.assertRedirects(response, reverse('reports_navigate'))

        # check if new report is displayed
        response = self.client.get(reverse('reports_new_report'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['reports']), 3)
        self.assertListEqual(
            list(response.context['reports']),
            sorted(
                list(response.context['reports']),
                key=lambda report: report.created_on,
                reverse=True
            )
        )

        full_coke = FullProduct.objects.get(product=self.coke.id, amount=10)
        full_green_tea = FullProduct.objects.get(
            product=self.green_tea.id,
            amount=20
        )
        self.assertEqual(full_coke.report, full_green_tea.report)

        new_report = full_coke.report
        self.assertIsNotNone(new_report)
        self.assertIsInstance(new_report, Report)
        self.assertTrue(new_report.created_on < timezone.now())
        self.assertEqual(new_report.creator, self.user)

    def test_edit_report_show(self):
        """Check if edit report is displayed properly."""

        response = self.client.get(
            reverse('reports_edit_report', args=(self.major_report.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_report.html')

        self.assertEqual(response.context['title'], u'Edytuj raport')

        full_products = FullProduct.objects.filter(report=self.major_report.id)
        report_products = [
            full_product.product for full_product in full_products
        ]

        products = json.loads(response.context['products'])
        all_products = Product.objects.all()

        for response_product in products:
            for product in all_products:
                if product.id != int(response_product['id']):
                    continue

                self.assertEqual(int(response_product['id']), product.id)
                self.assertEqual(str(response_product['name']), product.name)
                self.assertEqual(response_product['unit'], product.unit.name)

                if product in report_products:
                    self.assertEqual(bool(response_product['selected']), True)
                else:
                    self.assertEqual(bool(response_product['selected']), False)

    def test_edit_report_404(self):
        """Check if 404 is displayed when report does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('reports_edit_report', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('reports_edit_report', args=(_id,))

    def test_edit_report_post_fail(self):
        """Check if edit report fails to edit."""

        post = {}
        post[self.coke.id] = [self.coke.id, 10]
        post[self.green_tea.id] = [self.green_tea.id, 20]
        post[self.black_coffe.id] = [self.black_coffe.id, '']
        post['csrfmiddlewaretoken'] = 'hasz hasz hasz ####'

        response = self.client.post(
            reverse('reports_edit_report', args=(self.minor_report.id,)),
            post,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_report.html')
        self.assertIn('"errors": ["', response.context['products'])
        self.assertIn('To pole jest wymagane.', response.context['products'])

    def test_edit_report_post_success(self):
        """Check if edit report successes to edit."""

        post = {}
        post[self.coke.id] = [self.coke.id, 10]
        post[self.green_tea.id] = [self.green_tea.id, 20]
        post[self.black_coffe.id] = [self.black_coffe.id, 40]
        post['csrfmiddlewaretoken'] = 'hasz hasz hasz ####'

        response = self.client.post(
            reverse('reports_edit_report', args=(self.major_report.id,)),
            post,
            follow=True
        )

        self.assertRedirects(response, reverse('reports_navigate'))

        # check if report coffees has changed
        report = Report.objects.get(id=self.major_report.id)
        self.assertIsNotNone(report)
        self.assertIsInstance(report, Report)
        self.assertEqual(report.creator, self.user)

        full_products = FullProduct.objects.filter(report=self.major_report.id)
        self.assertEqual(len(full_products), 3)
        self.assertCountEqual(
            [full_product.product.id for full_product in full_products],
            [self.coke.id, self.green_tea.id, self.black_coffe.id]
        )
        self.assertCountEqual(
            [full_product.amount for full_product in full_products],
            [10, 20, 40]
        )

        # check if edited report is displayed
        response = self.client.get(reverse('reports_show_all_reports'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['reports']), 2)

    def test_report_navigate(self):
        """Check if create report view is displayed properly."""

        response = self.client.get(reverse('reports_navigate'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/reports.html')

    def test_show_all_reports_show(self):
        """Check if show all reports view actually shows all reports."""

        response = self.client.get(reverse('reports_show_all_reports'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/all.html')

        reports = Report.objects.order_by('-created_on')
        self.assertListEqual(list(response.context['reports']), list(reports))

    def test_show_report_show(self):
        """Check if show report view actually shows report."""

        response = self.client.get(
            reverse('reports_show_report', args=(self.major_report.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/show.html')

        report = Report.objects.get(id=self.major_report.id)
        self.assertEqual(response.context['report'], report)

        full_products = report.full_products.all()
        self.assertCountEqual(
            [self.cake_full_second, self.cake_full], list(full_products)
        )

        categories = response.context['categories']
        self.assertIn(self.cakes.name, categories)
        self.assertEqual(len(categories[self.cakes.name]), 2)

    def test_show_report_404(self):
        """Check if 404 is displayed when report does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('reports_show_report', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('reports_show_report', args=(_id,))

    def test_get_report_categories(self):
        """Check if display categories and products when report is valid."""

        categories = get_report_categories(self.major_report.id)
        full_products = self.major_report.full_products.all()

        for full_product in full_products:
            product = full_product.product
            self.assertIsNotNone(categories[product.category.name])
            self.assertIn(
                {
                    'name': product.name,
                    'amount': full_product.amount,
                    'unit': product.unit.name
                },
                categories[product.category.name]
            )

    def test_get_report_categories_invalid(self):
        """Check if does not display categories if report is invalid."""

        ids_invalid = [
            13, 23423, 24, 22, 242342322342, 2424242424224,
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_invalid:
            categories = get_report_categories(_id)
            self.assertIsNone(categories)
