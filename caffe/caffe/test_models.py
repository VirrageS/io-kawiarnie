"""Testing module for the Caffe model."""

from django.test import TestCase

from .models import Caffe
from employees.models import Employee


class CaffeModelTest(TestCase):
    """Caffe model tests."""

    def setUp(self):
        """Prepare database for tests."""

        self.user = Employee.objects.create(
            username='theboss',
            first_name='bossy',
            last_name='boss',
            telephone_number='12345678',
            email='boss@bosses.com',
            favorite_coffee='black'
        )

    def test_validation(self):
        """Validation tests for the Caffe model."""

        Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        with self.assertRaises(Exception):
            Caffe.objects.create(
                name='kafo',
                city='Gliwice',
                street='Wieczorka',
                house_number='14',
                building_number='100',
                postal_code='44-100',
                creator=self.user
            )

        with self.assertRaises(Exception):
            Caffe.objects.create(
                name='kafo2',
                city='Gliwice',
                street='Wieczorka',
                house_number='14',
                postal_code='44-100',
                creator=self.user
            )

    def test_str(self):
        """Test conversion to string."""

        Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100',
            creator=Employee.objects.get(username='theboss')
        )

        kafo = Caffe.objects.get(name='kafo')
        self.assertEqual(str(kafo), 'kafo, Gliwice')
