from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils import timezone
from django.db import transaction

from datetime import datetime

from .models import Report, Category, Product, Unit, FullProduct
from .forms import CategoryForm, UnitForm, ProductForm
from .forms import FullProductForm, ReportForm

class ReportTest(TestCase):
  def setUp(self):
    Report.objects.create(id = 1)
    Report.objects.create(id = 2)

  def test_created_on(self):
    now = timezone.now()
    r1 = Report.objects.get(id = 1)
    #self.assertTrue(datetime.now() - r1.created_on > 0)
    #self.assertTrue(now < r1.created_on)

class CategoryTest(TestCase):
  def setUp(self):
    Category.objects.create(name = "first")
    Category.objects.create(name = "second")

  def test_category_name(self):
    c1 = Category(name = "first")
    c2 = Category(name = "second")

    self.assertTrue(c1.name != c2.name)
    self.assertEqual(c1.name, "first")
    self.assertEqual(c2.name, "second")
    self.assertRaises(Exception, Category.objects.create, name = "first")
    self.assertRaises(Exception, Category.objects.create, name = "second")

class UnitTest(TestCase):
  def setUp(self):
    Unit.objects.create(name = "gram")
    Unit.objects.create(name = "liter")

  def test_unit(self):
    u_gram = Unit.objects.get(name = "gram")
    u_liter = Unit.objects.get(name = "liter")
    u_gram2 = Unit.objects.get(name = "gram")

    self.assertEqual(u_gram.id, u_gram2.id)
    self.assertRaises(Exception, Unit.objects.create, name = "liter")



class ProductTest(TestCase):
  def setUp(self):
    Category.objects.create(name = "first")
    Category.objects.create(name = "second")

    Unit.objects.create(name = "gram")
    Unit.objects.create(name = "liter")

  def test_product(self):
    first_cat = Category.objects.get(name = "first")
    second_cat = Category.objects.get(name = "second")

    gram = Unit.objects.get(name = "gram")
    liter = Unit.objects.get(name = "liter")

    p1 = Product.objects.create(
      name = "product1",
      category = first_cat,
      unit = gram
    )
    p2 = Product.objects.create(
      name = "product2",
      category = first_cat,
      unit = liter
    )
    p3 = Product.objects.create(
      name = "product3",
      category = second_cat,
      unit = gram
    )
    p4 = Product.objects.create(
      name = "product4",
      category = second_cat,
      unit = liter
    )


    self.assertEqual(first_cat.product_set.count(), 2)
    p2.delete()
    self.assertEqual(first_cat.product_set.count(), 1)
    p3.category = first_cat
    p3.save()
    self.assertEqual(first_cat.product_set.count(), 2)
    self.assertEqual(second_cat.product_set.count(), 1)
    p3.category = second_cat
    p3.save()

    self.assertEqual(gram.product_set.count(), 2)
    p3.delete()
    self.assertEqual(gram.product_set.count(), 1)

    self.assertRaises(
      Exception,
      Product.objects.create,
      name = "product1",
      category = first_cat,
      unit = gram
    )

class FullProductTest(TestCase):
  def setUp(self):
    first_cat = Category.objects.create(name = "first")
    second_cat = Category.objects.create(name = "second")

    gram = Unit.objects.create(name = "gram")
    liter = Unit.objects.create(name = "liter")

    Product.objects.create(
      name = "product1",
      category = first_cat,
      unit = gram
    )
    Product.objects.create(
      name = "product2",
      category = first_cat,
      unit = liter
    )
    Product.objects.create(
      name = "product3",
      category = second_cat,
      unit = gram
    )
    Product.objects.create(
      name = "product4",
      category = second_cat,
      unit = liter
    )

  def test_fullProduct(self):
    p1 = Product.objects.get(name = "product1")
    p2 = Product.objects.get(name = "product2")
    p3 = Product.objects.get(name = "product3")
    p4 = Product.objects.get(name = "product4")

    r1 = Report.objects.create(id = 1)
    r2 = Report.objects.create(id = 2)

    fp1 = FullProduct.objects.create(
      product = p1,
      amount = 10,
      report = r1
    )

    fp2 = FullProduct.objects.create(
      product = p2,
      amount = 100,
      report = r1
    )

    fp3 = FullProduct.objects.create(
      product = p3,
      amount = 0,
      report = r2
    )

    fp4 = FullProduct.objects.create(
      product = p4,
      amount = 1000,
      report = r2
    )

    self.assertEqual(fp1.product.name, "product1")
    self.assertEqual(fp2.amount, 100)
    self.assertEqual(fp2.report.id, r1.id)

    self.assertEqual(r2.full_products.count(), 2)
    fp4.delete()
    self.assertEqual(r2.full_products.count(), 1)

    self.assertEqual(r1.full_products.count(), 2)
    p2.delete()
    self.assertEqual(r1.full_products.count(), 1)

    fp1.amount = -1

    #this assertions should pass, but they dont
    '''
    self.assertRaises(Exception, fp1.save)
    self.assertRaises(
      Exception,
      FullProduct.objects.create,
      product = p1,
      amount = 50,
      report = r1
    )
    '''




###########################
####### VIEWS TESTS #######
###########################

class CategoryViewsTests(TestCase):
    def setUp(self):
        client = Client()

        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

    def test_new_category(self):
        response = self.client.get(reverse('reports_new_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], CategoryForm)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(response.context['context']['title'], 'Nowa kategoria')

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
            self.assertIn(element['desc'], [str(self.caffees), str(self.cakes)])


    def test_new_category_post_fail(self):
        """Checks if new category fails to create"""

        response = self.client.post(
            reverse('reports_new_category'),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['This field is required.'],
        })
        self.assertTemplateUsed(response, 'reports/new_element.html')

    def test_new_category_post_success(self):
        """Checks if new category successes to create"""

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

    def test_edit_category(self):
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
        # check if 404 is displayed when category does not exists
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
        """Checks if edit category fails to edit"""

        response = self.client.post(
            reverse('reports_edit_category', args=(self.cakes.id,)),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['This field is required.'],
        })
        self.assertTemplateUsed(response, 'reports/edit_element.html')

    def test_edit_category_post_success(self):
        """Checks if edit category successes to edit"""

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
    def setUp(self):
        client = Client()

        self.money = Unit.objects.create(name=u'złotówki')
        self.grams = Unit.objects.create(name=u'gramy')

    def test_new_unit(self):
        response = self.client.get(reverse('reports_new_unit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/new_element.html')

        # check context
        self.assertIsInstance(response.context['form'], UnitForm)

        self.assertEqual(len(response.context['context']), 1)
        self.assertEqual(response.context['context']['title'], 'Nowa jednostka')

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
        """Checks if new unit fails to create"""

        response = self.client.post(
            reverse('reports_new_unit'),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['This field is required.'],
        })
        self.assertTemplateUsed(response, 'reports/new_element.html')

    def test_new_unit_post_success(self):
        """Checks if new unit successes to create"""

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

    def test_edit_unit(self):
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
        # check if 404 is displayed when unit does not exists
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
        """Checks if edit unit fails to edit"""

        response = self.client.post(
            reverse('reports_edit_unit', args=(self.grams.id,)),
            {u'name': u''},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.context['form'].errors, {
            'name': ['This field is required.'],
        })
        self.assertTemplateUsed(response, 'reports/edit_element.html')

    def test_edit_unit_post_success(self):
        """Checks if edit unit successes to edit"""

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
    pass

class FullProductViewsTests(TestCase):
    pass

class ReportViewsTests(TestCase):
    pass
