from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from employees.models import Employee


class CaffeViewsTests(TestCase):
    """Test all views of the landing page."""

    def setUp(self):
        """Initialize all Caffe needed in tests."""

        self.client = Client()

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin'
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='view_cashreport'),
            Permission.objects.get(codename='view_workedhours'),
        )

    def test_landing_logged_out(self):
        """Check if landing page appears if user is not logged in."""

        response = self.client.get(reverse('index_navigate'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/landing_page.html')

    def test_landing_logged_in(self):
        """Check if landing page redirect if user is logged in."""

        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('index_navigate'), follow=True)
        self.assertRedirects(response, reverse('home:navigate'))
