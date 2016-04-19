# -*- encoding: utf-8 -*-

from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils import timezone

from .models import Report, Category, Product, Unit, FullProduct
from .forms import CategoryForm, UnitForm, ProductForm
from .forms import FullProductForm, ReportForm


class CategoryViewsTests(TestCase):
    """Tests all views for Category model."""

    def setUp(self):
        self.client = Client()

        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

    def test_new_category_show(self):
        """Checks if new category view is displayed properly."""

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

        for element in elements:
            self.assertEqual(len(element), 3)
            self.assertIn(
                element['edit_href'], [
                    reverse('reports_edit_category', args=(self.caffees.id,)),
                    reverse('reports_edit_category', args=(self.cakes.id,))
                ]
            )
            self.assertIn(element['id'], [self.caffees.id, self.cakes.id])
            self.assertIn(
                element['desc'],
                [str(self.caffees), str(self.cakes)]
            )

    def test_new_category_post_fail(self):
        """Checks if new category fails to create when form is not valid."""

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
        """Checks if new category successes to create when form is valid."""

        response = self.client.post(
            reverse('reports_new_category'),
            {u'name': u'Napoje'},
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if new category is displayed
        response = self.client.get(reverse('reports_new_category'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)

        new_category = Category.objects.get(name='Napoje')
        self.assertIsNotNone(new_category)
        self.assertIsInstance(new_category, Category)

    def test_edit_category_show(self):
        """Checks if edit category view is displayed properly"""

        response = self.client.get(
            reverse('reports_edit_category', args=(self.caffees.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, CategoryForm)
        self.assertEqual(form.instance, self.caffees)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj kategorię'
        )

    def test_edit_category_404(self):
        """Checks if 404 is displayed when category does not exists."""

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
        """Checks if edit category fails to edit when form is not valid."""

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
        """Checks if edit category successes to edit when form is valid."""

        response = self.client.post(
            reverse('reports_edit_category', args=(self.cakes.id,)),
            {u'name': u'Napoje'},
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if category caffees has changed
        category = Category.objects.get(id=self.cakes.id)
        self.assertEqual(category.name, u'Napoje')

        # check if edited category is displayed
        response = self.client.get(reverse('reports_new_category'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class UnitViewsTests(TestCase):
    """Tests all views for Unit model."""

    def setUp(self):
        self.client = Client()

        self.money = Unit.objects.create(name=u'złotówki')
        self.grams = Unit.objects.create(name=u'gramy')

    def test_new_unit_show(self):
        """Checks if new unit view is displayed properly."""

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
        """Checks if new unit fails to create when form is not valid."""

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
        """Checks if new unit successes to create if form is valid."""

        response = self.client.post(
            reverse('reports_new_unit'),
            {u'name': u'sztuki'},
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if new unit is displayed
        response = self.client.get(reverse('reports_new_unit'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)

        new_unit = Unit.objects.get(name='sztuki')
        self.assertIsNotNone(new_unit)
        self.assertIsInstance(new_unit, Unit)

    def test_edit_unit_show(self):
        """Checks if edit unit view is displayed properly."""

        response = self.client.get(
            reverse('reports_edit_unit', args=(self.money.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, UnitForm)
        self.assertEqual(form.instance, self.money)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj jednostkę'
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
        """Checks if edit unit fails to edit when form is not valid."""

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
        """Checks if edit unit successes to edit when form is valid."""

        response = self.client.post(
            reverse('reports_edit_unit', args=(self.grams.id,)),
            {u'name': u'sztuki'},
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if unit caffees has changed
        unit = Unit.objects.get(id=self.grams.id)
        self.assertEqual(unit.name, u'sztuki')

        # check if edited unit is displayed
        response = self.client.get(reverse('reports_new_unit'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class ProductViewsTests(TestCase):
    """Tests all views for Product model."""

    def setUp(self):
        self.client = Client()

        self.grams = Unit.objects.create(name=u'gramy')
        self.pieces = Unit.objects.create(name=u'sztuki')

        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

        self.caffee = Product.objects.create(
            name='Kawa sypana',
            category=self.caffees,
            unit=self.grams
        )

        self.cake = Product.objects.create(
            name='Szarlotka',
            category=self.cakes,
            unit=self.pieces
        )

    def test_new_product_show(self):
        """Checks if new product view is displayed properly."""

        response = self.client.get(reverse('reports_new_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], ProductForm)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(response.context['context']['title'], 'Nowy produkt')

        elements = response.context['elements']
        self.assertEqual(len(elements), 2)

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
        """Checks if new product fails to create when form is not valid."""

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
        """Checks if new product successes to create when form is valid."""

        response = self.client.post(
            reverse('reports_new_product'), {
                'name': u'Sernik',
                'category': self.cakes.id,
                'unit': self.pieces.id
            },
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if new product is displayed
        response = self.client.get(reverse('reports_new_product'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)

        new_product = Product.objects.get(name=u'Sernik')
        self.assertIsNotNone(new_product)
        self.assertIsInstance(new_product, Product)
        self.assertEqual(new_product.category, self.cakes)
        self.assertEqual(new_product.unit, self.pieces)

    def test_edit_product_show(self):
        """Checks if edit product view is displayed properly."""

        response = self.client.get(
            reverse('reports_edit_product', args=(self.caffee.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, ProductForm)
        self.assertEqual(form.instance, self.caffee)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj produkt'
        )

    def test_edit_product_404(self):
        """Checks if 404 is displayed when product does not exists."""

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
        """Checks if edit product fails to edit when form is not valid."""

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
        """Checks if edit product successes to edit when form is valid."""

        response = self.client.post(
            reverse('reports_edit_product', args=(self.cake.id,)), {
                'name': u'Keks',
                'category': self.cakes.id,
                'unit': self.pieces.id
            },
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if product caffees has changed
        product = Product.objects.get(id=self.cake.id)
        self.assertEqual(product.name, u'Keks')
        self.assertEqual(product.category, self.cakes)
        self.assertEqual(product.unit, self.pieces)

        # check if edited product is displayed
        response = self.client.get(reverse('reports_new_product'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class FullProductViewsTests(TestCase):
    """Tests all views for FullProduct model."""

    def setUp(self):
        self.client = Client()

        self.grams = Unit.objects.create(name=u'gramy')
        self.pieces = Unit.objects.create(name=u'sztuki')

        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

        self.caffee = Product.objects.create(
            name='Kawa sypana',
            category=self.caffees,
            unit=self.grams
        )

        self.cake = Product.objects.create(
            name='Szarlotka',
            category=self.cakes,
            unit=self.pieces
        )

        self.caffee_full = FullProduct.objects.create(
            product=self.caffee,
            amount=50
        )

        self.cake_full = FullProduct.objects.create(
            product=self.cake,
            amount=10
        )

    def test_new_fullproduct_show(self):
        """Checks if new FullProduct view is displayed properly."""

        response = self.client.get(reverse('reports_new_fullproduct'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_fullproduct.html')

        # check context
        self.assertIsInstance(response.context['form'], FullProductForm)
        self.assertEqual(len(response.context['context']), 0)

        products_count = Product.objects.count()
        self.assertEqual(len(response.context['products']), products_count)

        for product in response.context['products']:
            product_found = Product.objects.get(id=product['id'])
            self.assertIsNotNone(product_found)
            self.assertIsInstance(product_found, Product)
            self.assertEqual(product_found.unit.name, product['unit'])

        elements = response.context['elements']
        self.assertEqual(len(elements), 2)

        for element in elements:
            self.assertEqual(len(element), 3)
            self.assertIn(
                element['edit_href'], [
                    reverse(
                        'reports_edit_fullproduct',
                        args=(self.caffee_full.id,)
                    ),
                    reverse(
                        'reports_edit_fullproduct',
                        args=(self.cake_full.id,)
                    )
                ]
            )

            self.assertIn(
                element['id'],
                [self.caffee_full.id, self.cake_full.id]
            )

            self.assertIn(
                element['desc'],
                [str(self.caffee_full), str(self.cake_full)]
            )

    def test_new_fullproduct_post_fail(self):
        """Checks if new fullproduct fails to create when form is not valid."""

        response = self.client.post(
            reverse('reports_new_fullproduct'),
            {'amount': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'product': ['To pole jest wymagane.'],
            'amount': ['To pole jest wymagane.'],
        })
        self.assertTemplateUsed(response, 'reports/new_fullproduct.html')

    def test_new_fullproduct_post_success(self):
        """Checks if new fullproduct successes to create when form is valid."""

        response = self.client.post(
            reverse('reports_new_fullproduct'),
            {
                'product': self.cake.id,
                'amount': 5000
            },
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if new fullproduct is displayed
        response = self.client.get(reverse('reports_new_fullproduct'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)

        new_fullproduct = FullProduct.objects.get(amount=5000)
        self.assertIsNotNone(new_fullproduct)
        self.assertIsInstance(new_fullproduct, FullProduct)
        self.assertEqual(new_fullproduct.product, self.cake)
        self.assertEqual(new_fullproduct.amount, 5000)

    def test_edit_fullproduct_show(self):
        """Checks if edit FullProduct view is displayed properly."""

        response = self.client.get(
            reverse('reports_edit_fullproduct', args=(self.caffee_full.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/edit_fullproduct.html')

        form = response.context['form']
        self.assertIsInstance(form, FullProductForm)
        self.assertEqual(form.instance, self.caffee_full)

        self.assertEqual(len(response.context['context']), 0)

        products_count = Product.objects.count()
        self.assertEqual(len(response.context['products']), products_count)

        for product in response.context['products']:
            product_found = Product.objects.get(id=product['id'])
            self.assertIsNotNone(product_found)
            self.assertIsInstance(product_found, Product)
            self.assertEqual(product_found.unit.name, product['unit'])

    def test_edit_fullproduct_404(self):
        """Checks if 404 is displayed when fullproduct does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            response = self.client.get(
                reverse('reports_edit_fullproduct', args=(_id,))
            )
            self.assertEqual(response.status_code, 404)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('reports_edit_fullproduct', args=(_id,))

    def test_edit_fullproduct_post_fail(self):
        """Checks if edit fullproduct fails to edit when form is not valid."""

        response = self.client.post(
            reverse('reports_edit_fullproduct', args=(self.cake_full.id,)),
            {'amount': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'product': ['To pole jest wymagane.'],
            'amount': ['To pole jest wymagane.']
        })
        self.assertTemplateUsed(response, 'reports/edit_fullproduct.html')

    def test_edit_fullproduct_post_success(self):
        """Checks if edit fullproduct successes to edit when form is valid."""

        response = self.client.post(
            reverse('reports_edit_fullproduct', args=(self.cake_full.id,)),
            {
                'product': self.cake.id,
                'amount': 5000
            },
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if fullproduct caffees has changed
        fullproduct = FullProduct.objects.get(id=self.cake_full.id)
        self.assertEqual(fullproduct.product, self.cake)
        self.assertEqual(fullproduct.amount, 5000)

        # check if edited fullproduct is displayed
        response = self.client.get(reverse('reports_new_fullproduct'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)


class ReportViewsTests(TestCase):
    """Tests all views for Report model."""

    def setUp(self):
        self.client = Client()

        self.grams = Unit.objects.create(name=u'gramy')
        self.pieces = Unit.objects.create(name=u'sztuki')

        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

        self.caffee = Product.objects.create(
            name='Kawa sypana',
            category=self.caffees,
            unit=self.grams
        )

        self.cake = Product.objects.create(
            name='Szarlotka',
            category=self.cakes,
            unit=self.pieces
        )

        self.caffee_full = FullProduct.objects.create(
            product=self.caffee,
            amount=50
        )

        self.caffee_full_second = FullProduct.objects.create(
            product=self.caffee,
            amount=40
        )

        self.cake_full = FullProduct.objects.create(
            product=self.cake,
            amount=10
        )

        self.cake_full_second = FullProduct.objects.create(
            product=self.cake,
            amount=50
        )

        self.minor_report = Report.objects.create()
        self.major_report = Report.objects.create()

        self.caffee_full.report = self.minor_report
        self.caffee_full.save()

        self.caffee_full_second.report = self.major_report
        self.cake_full.report = self.major_report
        self.caffee_full_second.save()
        self.cake_full.save()

    def test_new_report_show(self):
        """Checks if new report view is displayed properly"""

        response = self.client.get(reverse('reports_new_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], ReportForm)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            'Nowy raport'
        )

        elements = response.context['elements']
        self.assertEqual(len(elements), 2)

        for element in elements:
            self.assertEqual(len(element), 3)
            self.assertIn(
                element['edit_href'], [
                    reverse(
                        'reports_edit_report',
                        args=(self.minor_report.id,)
                    ),
                    reverse(
                        'reports_edit_report',
                        args=(self.major_report.id,)
                    )
                ]
            )

            self.assertIn(
                element['id'],
                [self.minor_report.id, self.major_report.id]
            )

            self.assertIn(
                element['desc'],
                [str(self.minor_report), str(self.major_report)]
            )

    def test_new_report_post_fail(self):
        """Checks if new report fails to create when form is not valid."""

        response = self.client.post(
            reverse('reports_new_report'),
            {'full_products': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(
            response.context['form'].errors, {
                'full_products':
                    ['"" nie jest poprawną wartością klucza głównego.']
            }
        )
        self.assertTemplateUsed(response, 'reports/new_element.html')

    def test_new_report_post_success(self):
        """Checks if new report successes to create"""

        response = self.client.post(
            reverse('reports_new_report'),
            {
                'full_products': [self.cake_full_second.id],
            },
            follow=True
        )

        # print(response.context['form'])
        self.assertRedirects(response, reverse('reports_create'))

        # check if new report is displayed
        response = self.client.get(reverse('reports_new_report'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 3)

        cake = FullProduct.objects.get(id=self.cake_full_second.id)
        new_report = cake.report
        self.assertIsNotNone(new_report)
        self.assertIsInstance(new_report, Report)
        self.assertTrue(new_report.created_on < timezone.now())

    def test_edit_report_show(self):
        """Checks if edit report is displayed properly"""

        response = self.client.get(
            reverse('reports_edit_report', args=(self.major_report.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/edit_element.html')

        form = response.context['form']
        self.assertIsInstance(form, ReportForm)
        self.assertEqual(form.instance, self.major_report)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(
            response.context['context']['title'],
            u'Edytuj raport'
        )

    def test_edit_report_404(self):
        """Checks if 404 is displayed when report does not exists."""

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
        """Checks if edit report fails to edit"""

        response = self.client.post(
            reverse('reports_edit_report', args=(self.major_report.id,)),
            {'full_products': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(
            response.context['form'].errors, {
                'full_products':
                    ['"" nie jest poprawną wartością klucza głównego.']
            }
        )
        self.assertTemplateUsed(response, 'reports/edit_element.html')

    def test_edit_report_post_success(self):
        """Checks if edit report successes to edit"""

        response = self.client.post(
            reverse('reports_edit_report', args=(self.caffee_full_second.id,)),
            {
                'full_products': [self.cake_full_second.id],
            },
            follow=True
        )

        self.assertRedirects(response, reverse('reports_create'))

        # check if report caffees has changed
        report = FullProduct.objects.get(id=self.cake_full_second.id).report
        self.assertIsNotNone(report)
        self.assertIsInstance(report, Report)

        # check if edited report is displayed
        response = self.client.get(reverse('reports_new_report'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['elements']), 2)

    def test_create_report(self):
        """Checks if create report view is displayed properly"""

        response = self.client.get(reverse('reports_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/create_report.html')

    def test_show_all_reports_show(self):
        """Checks if show all reports view actually shows all reports"""

        response = self.client.get(reverse('reports_show_all'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/all.html')

        reports = Report.objects.all()
        self.assertListEqual(list(response.context['reports']), list(reports))

    def test_show_report_show(self):
        """Checks if show report view actually shows report"""

        response = self.client.get(
            reverse('reports_show_report', args=(self.major_report.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/show.html')

        report = Report.objects.get(id=self.major_report.id)
        self.assertEqual(response.context['report'], report)

        full_products = report.full_products.all()
        self.assertListEqual(
            [self.caffee_full_second, self.cake_full], list(full_products)
        )

        categories = response.context['categories']
        self.assertIn(self.caffees.name, categories)
        self.assertIn(self.cakes.name, categories)

        self.assertEqual(len(categories[self.caffees.name]), 1)
        self.assertEqual(len(categories[self.cakes.name]), 1)

    def test_show_report_404(self):
        """Checks if 404 is displayed when report does not exists."""

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
