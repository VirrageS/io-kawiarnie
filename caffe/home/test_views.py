from datetime import date, datetime

from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.utils import timezone

from caffe.models import Caffe
from cash.models import CashReport
from employees.models import Employee
from hours.models import Position, WorkedHours
from reports.models import Report


class CaffeViewsTests(TestCase):
    """Test all views of the caffe."""

    def setUp(self):
        """Initialize all Caffe needed in tests."""

        self.client = Client()

        self.kafo = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin',
            caffe=self.kafo
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='view_cashreport'),
            Permission.objects.get(codename='view_workedhours'),
        )

        self.client.login(username='admin', password='admin')

        # objects
        self.main_report = Report.objects.create(caffe=self.kafo)
        self.minor_report = Report.objects.create(caffe=self.kafo)

        self.cash_report_main = CashReport(
            cash_before_shift=1000,
            cash_after_shift=1200,
            card_payments=123,
            amount_due=100,
            creator=self.user,
            caffe=self.kafo
        )
        self.cash_report_main.save()

        self.cash_report_minor = CashReport(
            cash_before_shift=1001,
            cash_after_shift=1201,
            card_payments=124,
            amount_due=50,
            creator=self.user,
            caffe=self.kafo
        )
        self.cash_report_minor.save()
        self.cash_report_minor.created_on = timezone.make_aware(
            datetime(2015, 6, 3, 10, 0),
            timezone.get_current_timezone()
        )
        self.cash_report_minor.save()

        self.barista = Position.objects.create(name='Barista', caffe=self.kafo)

        self.worked_hours_main = WorkedHours(
            start_time='12:30',
            end_time='15:50',
            date=date.today(),
            position=self.barista,
            employee=self.user
        )
        self.worked_hours_main.save()

        self.worked_hours_minor = WorkedHours(
            start_time='18:30',
            end_time='20:50',
            date=date(2015, 5, 3),
            position=self.barista,
            employee=self.user
        )
        self.worked_hours_minor.save()

    def test_caffe_navigate(self):
        """Check if caffe view (today view) is displayed properly."""

        response = self.client.get(reverse('caffe_navigate'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/caffe.html')

        self.assertCountEqual(
            response.context['reports'],
            [self.main_report, self.minor_report]
        )

        self.assertCountEqual(
            response.context['cash_reports'],
            [self.cash_report_main]
        )

        self.assertCountEqual(
            response.context['worked_hours'],
            [self.worked_hours_main]
        )
