# -*- encoding: utf-8 -*-

from django.core.urlresolvers import NoReverseMatch, reverse
from django.test import Client, TestCase
from django.utils import timezone

from reports.models import Category


class StencilViewTests(TestCase):
    """Tests all views for Stencil model."""

    def setUp(self):
        """test data setup """
        self.client = Client()

        self.caffees = Category.objects.create(name='Kawy')
        self.cakes = Category.objects.create(name='Ciasta')

    def test_new_category_show(self):
        """Check if new category view is displayed properly."""

        pass
