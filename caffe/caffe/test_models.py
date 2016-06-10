"""Testing module for the Caffe model."""

from django.test import TestCase

from .models import Caffe


class CaffeModelTest(TestCase):
    """Caffe model tests."""

    def setUp(self):
        """Prepare database for tests."""

        Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

    def test_validation(self):
        """Validation tests for the Caffe model."""

        with self.assertRaises(Exception):
            Caffe.objects.create(
                name='kafo',
                city='Gliwice',
                street='Wieczorka',
                house_number='14',
                postal_code='44-100'
            )

    def test_str(self):
        """Test conversion to string."""

        kafo = Caffe.objects.get(name='kafo')

        self.assertEqual(str(kafo), 'kafo, Gliwice')
