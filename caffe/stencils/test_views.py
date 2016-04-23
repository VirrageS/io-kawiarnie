# -*- encoding: utf-8 -*-

from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils import timezone

from reports.models import Category


class StencilViewTests(TestCase):
    """Tests all views for Stencil model."""

    def setUp(self):
        self.client = Client()

        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

    def test_new_category_show(self):
        """Checks if new category view is displayed properly."""

        pass
