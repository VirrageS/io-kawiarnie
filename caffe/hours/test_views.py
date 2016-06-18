from datetime import date, time

from django.contrib.auth.models import Permission
from django.core.urlresolvers import NoReverseMatch, reverse
from django.test import Client, RequestFactory, TestCase
from django.http import Http404

from employees.models import Employee

from .forms import PositionForm, WorkedHoursForm
from .models import Position, WorkedHours
from .views import hours_edit_position, hours_new_position,\
    hours_edit_worked_hours, hours_new_worked_hours
from caffe.models import Caffe


class PositionViewsTests(TestCase):
    """Test all views of the Position model."""

    def setUp(self):
        """Initialize all Position needed in tests."""

        self.client = Client()

        self.kafo = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        self.barista = Position.objects.create(name='Barista', caffe=self.kafo)
        self.cleaning = Position.objects.create(name='Sprzątanie',
                                                caffe=self.kafo)

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin',
            caffe=self.kafo
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_position'),
            Permission.objects.get(codename='change_position'),
            Permission.objects.get(codename='view_position'),

            Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='view_cashreport'),
            Permission.objects.get(codename='view_workedhours'),
        )

        self.client.login(username='admin', password='admin')

        self.factory = RequestFactory()

    def test_new_position_show(self):
        """Check if new Position view is displayed properly."""

        request = self.factory.get(reverse('new_position'))
        request.user = self.user
        response = hours_new_position(request)

        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'hours/new_position.html')
        #
        # # check context
        # self.assertIsInstance(response.context['form'], PositionForm)
        # self.assertEqual(response.context['title'], 'Nowe stanowisko')
        # self.assertEqual(response.context['button'], 'Dodaj')
        #
        # positions = response.context['positions']
        # self.assertEqual(len(positions), 2)
        # self.assertListEqual(
        #     positions,
        #     sorted(positions, key=lambda x: x['desc'], reverse=False)
        # )
        #
        # for position in positions:
        #     self.assertEqual(len(position), 2)
        #     self.assertIn(position['id'], [self.barista.id, self.cleaning.id])
        #     self.assertIn(
        #         position['desc'],
        #         [str(self.barista), str(self.cleaning)]
        #     )

    def test_new_position_post_fail(self):
        """Check if new Position fails to create when form is not valid."""

        request = self.factory.post(reverse('new_position'), {u'name': u''})
        request.user = self.user
        response = hours_new_position(request)

        # response = self.client.post(
        #     reverse('new_position'),
        #     {u'name': u''},
        #     follow=True
        # )

        self.assertEqual(response.status_code, 200)
        # self.assertFalse(response.context['form'].is_valid())
        # self.assertEqual(response.context['form'].errors, {
        #     'name': ['To pole jest wymagane.'],
        # })
        # self.assertTemplateUsed(response, 'hours/new_position.html')

    def test_new_position_post_success(self):
        """Check if new Position successes to create when form is valid."""

        # response = self.client.post(
        #     reverse('new_position'),
        #     {u'name': u'Kasa'},
        #     follow=True
        # )

        request = self.factory.post(reverse('new_position'),
                                    {u'name': u'Kasa'})
        request.user = self.user
        response = hours_new_position(request)

        # self.assertRedirects(response, reverse('caffe_navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        # check if new category is displayed
        # response = self.client.get(reverse('new_position'))

        request = self.factory.get(reverse('new_position'))
        request.user = self.user
        response = hours_new_position(request)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.context['positions']), 3)
        # self.assertListEqual(
        #     response.context['positions'],
        #     sorted(
        #         response.context['positions'],
        #         key=lambda x: x['desc'],
        #         reverse=False
        #     )
        # )

        new_position = Position.objects.get(name='Kasa')
        self.assertIsNotNone(new_position)
        self.assertIsInstance(new_position, Position)

    def test_edit_position_show(self):
        """Check if edit Position view is displayed properly."""

        # response = self.client.get(
        #     reverse('edit_position', args=(self.barista.id,))
        # )

        request = self.factory.get(reverse('edit_position',
                                           args=(self.barista.id,)))
        request.user = self.user
        response = hours_edit_position(request, self.barista.id)

        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'hours/new_position.html')

        # form = response.context['form']
        # self.assertIsInstance(form, PositionForm)
        # self.assertEqual(form.instance, self.barista)
        #
        # self.assertEqual(response.context['title'], u'Edytuj stanowisko')
        # self.assertEqual(response.context['button'], u'Uaktualnij')

    def test_edit_position_404(self):
        """Check if 404 is displayed when Position does not exists."""

        ids_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        ids_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _id in ids_for_404:
            # response = self.client.get(
            #     reverse('edit_position', args=(_id,))
            # )

            request = self.factory.get(reverse('edit_position', args=(_id,)))
            request.user = self.user
            with self.assertRaises(Http404):
                hours_edit_position(request, _id)

        for _id in ids_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('edit_position', args=(_id,))

    def test_edit_position_post_fail(self):
        """Check if edit Position fails to edit when form is not valid."""

        # response = self.client.post(
        #     reverse('edit_position', args=(self.barista.id,)),
        #     {u'name': u''},
        #     follow=True
        # )

        request = self.factory.post(reverse('edit_position',
                                            args=(self.barista.id,)),
                                    {u'name': u''})
        request.user = self.user
        response = hours_edit_position(request, self.barista.id)

        self.assertEqual(response.status_code, 200)
        # self.assertFalse(response.context['form'].is_valid())
        # self.assertEqual(response.context['form'].errors, {
        #     'name': ['To pole jest wymagane.'],
        # })
        # self.assertTemplateUsed(response, 'hours/new_position.html')

    def test_edit_position_post_success(self):
        """Check if edit position successes to edit when form is valid."""

        # response = self.client.post(
        #     reverse('edit_position', args=(self.barista.id,)),
        #     {u'name': u'Bar'},
        #     follow=True
        # )

        request = self.factory.post(reverse('edit_position',
                                            args=(self.barista.id,)),
                                    {u'name': u'Bar'})
        request.user = self.user
        response = hours_edit_position(request, self.barista.id)

        # self.assertRedirects(response, reverse('caffe_navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        # check if position has changed
        position = Position.objects.get(id=self.barista.id)
        self.assertEqual(position.name, u'Bar')

        # check if edited position is displayed
        # response = self.client.get(reverse('new_position'))

        request = self.factory.get(reverse('new_position'))
        request.user = self.user
        response = hours_new_position(request)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.context['positions']), 2)


class WorkedHoursViewsTests(TestCase):
    """Test all views of the WorkedHours model."""

    def setUp(self):
        """Initialize all WorkedHours needed in tests."""

        self.client = Client()
        self.factory = RequestFactory()

        self.kafo = Caffe.objects.create(
            name='kafo',
            city='Gliwice',
            street='Wieczorka',
            house_number='14',
            postal_code='44-100'
        )

        self.barista = Position.objects.create(name='Barista', caffe=self.kafo)
        self.cleaning = Position.objects.create(name='Sprzątanie',
                                                caffe=self.kafo)

        self.worked_hours_main = WorkedHours(
            start_time='12:30',
            end_time='15:50',
            date='2016-06-01',
            position=self.barista
        )

        # add user and permissions
        self.user = Employee.objects.create_user(
            username='admin',
            password='admin',
            caffe=self.kafo
        )
        self.user.save()
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_workedhours'),
            Permission.objects.get(codename='change_workedhours'),
            Permission.objects.get(codename='view_workedhours'),

            Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='view_cashreport'),
        )

        self.user_second = Employee.objects.create_user(
            username='admin1',
            password='admin1',
            caffe=self.kafo
        )
        self.user_second.save()
        self.user_second.user_permissions.add(
            Permission.objects.get(codename='add_workedhours'),
            Permission.objects.get(codename='change_workedhours'),
            Permission.objects.get(codename='view_workedhours'),
        )

        self.admin = Employee.objects.create_user(
            username='sadmin',
            password='sadmin',
            caffe=self.kafo
        )
        self.admin.save()
        self.admin.user_permissions.add(
            Permission.objects.get(codename='add_workedhours'),
            Permission.objects.get(codename='change_workedhours'),
            Permission.objects.get(codename='view_workedhours'),
            Permission.objects.get(codename='change_all_workedhours'),

            Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='view_cashreport'),
        )

        self.client.login(username='admin', password='admin')

        self.worked_hours_main.employee = self.user
        self.worked_hours_main.save()

    def test_new_workedhours_show(self):
        """Check if new WorkedHours view is displayed properly."""

        # response = self.client.get(reverse('new_worked_hours'))
        request = self.factory.get(reverse('new_worked_hours'))
        request.user = self.user
        response = hours_new_worked_hours(request)

        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'hours/new_hours.html')
        #
        # # check context
        # self.assertIsInstance(response.context['form'], WorkedHoursForm)
        # self.assertEqual(
        #     response.context['title'],
        #     'Nowe przepracowane godziny'
        # )
        # self.assertEqual(response.context['button'], 'Dodaj')

    def test_new_workedhours_post_fail(self):
        """Check if new WorkedHours fails to create when form is not valid."""

        # response = self.client.post(
        #     reverse('new_worked_hours'),
        #     {
        #         'start_time': '12:00',
        #         'end_time': '',
        #         'date': '31.05.2016',
        #         'position': self.barista.id
        #     },
        #     follow=True
        # )
        form = {
            'start_time': '12:00',
            'end_time': '',
            'date': '31.05.2016',
            'position': self.barista.id
        }
        request = self.factory.post(reverse('new_worked_hours'), form)
        request.user = self.user
        response = hours_new_worked_hours(request)

        self.assertEqual(response.status_code, 200)
        # self.assertFalse(response.context['form'].is_valid())
        # self.assertEqual(response.context['form'].errors, {
        #     'end_time': ['To pole jest wymagane.'],
        # })
        # self.assertTemplateUsed(response, 'hours/new_hours.html')

    def test_new_workedhours_post_success(self):
        """Check if new WorkedHours successes to create when form is valid."""

        # response = self.client.post(
        #     reverse('new_worked_hours'),
        #     {
        #         'start_time': '21:00',
        #         'end_time': '22:00',
        #         'date': '31.05.2016',
        #         'position': self.barista.id
        #     },
        #     follow=True
        # )
        form = {
            'start_time': '21:00',
            'end_time': '22:00',
            'date': '31.05.2016',
            'position': self.barista.id
        }
        request = self.factory.post(reverse('new_worked_hours'), form)
        request.user = self.user
        response = hours_new_worked_hours(request)

        # self.assertRedirects(response, reverse('caffe_navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        # check if new worked_hours is displayed
        new_worked_hours = WorkedHours.objects.get(start_time='21:00')
        self.assertIsNotNone(new_worked_hours)
        self.assertIsInstance(new_worked_hours, WorkedHours)
        self.assertEqual(new_worked_hours.employee, self.user)

    def test_edit_workedhours_show(self):
        """Check if edit WorkedHours view is displayed properly."""

        # response = self.client.get(
        #     reverse('edit_worked_hours', args=(self.worked_hours_main.pk,))
        # )

        request = self.factory.get(reverse('edit_worked_hours',
                                           args=(self.worked_hours_main.pk,)))
        request.user = self.user
        response = hours_edit_worked_hours(request, self.worked_hours_main.pk)

        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'hours/new_hours.html')

        # form = response.context['form']
        # self.assertIsInstance(form, WorkedHoursForm)
        # self.assertEqual(form.instance, self.worked_hours_main)
        #
        # self.assertEqual(
        #     response.context['title'],
        #     'Edytuj przepracowane godziny'
        # )
        # self.assertEqual(response.context['button'], 'Uaktualnij')

    def test_edit_workedhours_404(self):
        """Check if 404 is displayed when WorkedHours does not exists."""

        pks_for_404 = [13, 23423, 24, 22, 242342322342, 2424242424224]
        pks_could_not_resolve = [
            -1, -234234, 234.32224, "werwe", 242342394283409284023840394823
        ]

        for _pk in pks_for_404:
            request = self.factory.get(reverse('edit_worked_hours',
                                               args=(_pk,)))
            request.user = self.user
            with self.assertRaises(Http404):
                hours_edit_worked_hours(request, _pk)

            # response = self.client.get(
            #     reverse('edit_worked_hours', args=(_pk,))
            # )
            # self.assertEqual(response.status_code, 404)

        for _pk in pks_could_not_resolve:
            with self.assertRaises(NoReverseMatch):
                reverse('edit_worked_hours', args=(_pk,))

    def test_edit_workedhours_post_fail(self):
        """Check if edit WorkedHours fails to edit when form is not valid."""

        # response = self.client.post(
        #     reverse('edit_worked_hours', args=(self.worked_hours_main.pk,)),
        #     {
        #         'start_time': '21:00',
        #         'end_time': '',
        #         'date': '3105.2016',
        #         'position': self.barista.id
        #     },
        #     follow=True
        # )
        form = {
            'start_time': '21:00',
            'end_time': '',
            'date': '3105.2016',
            'position': self.barista.id
        }

        request = self.factory.post(reverse('edit_worked_hours',
                                            args=(self.worked_hours_main.pk,)),
                                    form)
        request.user = self.user
        response = hours_edit_worked_hours(request, self.worked_hours_main.pk)

        self.assertEqual(response.status_code, 200)
        # self.assertFalse(response.context['form'].is_valid())
        # self.assertEqual(response.context['form'].errors, {
        #     'end_time': ['To pole jest wymagane.'],
        #     'date': ['Wpisz poprawną datę.'],
        # })
        # self.assertTemplateUsed(response, 'hours/new_hours.html')

    def test_edit_workedhours_denied_access(self):
        """Check if edit WorkedHours fails if someone else tries to modify."""

        self.client.login(username='admin1', password='admin1')

        # response = self.client.post(
        #     reverse('edit_worked_hours', args=(self.worked_hours_main.pk,)),
        #     {
        #         'start_time': '21:00',
        #         'end_time': '22:00',
        #         'date': '31.05.2016',
        #         'position': self.barista.id
        #     },
        #     follow=True
        # )
        form = {
            'start_time': '21:00',
            'end_time': '22:00',
            'date': '31.05.2016',
            'position': self.barista.id
        }

        request = self.factory.post(reverse('edit_worked_hours',
                                            args=(self.worked_hours_main.pk,)),
                                    form)
        request.user = self.user_second

        with self.assertRaises(Http404):
            hours_edit_worked_hours(request, self.worked_hours_main.pk)

        # self.assertEqual(response.status_code, 404)

    def test_edit_workedhours_admin_access(self):
        """Check if edit WorkedHours succeeds if admin tries to modify."""

        self.client.login(username='sadmin', password='sadmin')

        response = self.client.post(
            reverse('edit_worked_hours', args=(self.worked_hours_main.pk,)),
            {
                'start_time': '21:00',
                'end_time': '22:00',
                'date': '31.05.2016',
                'position': self.barista.id
            },
            follow=True
        )

        self.assertRedirects(response, reverse('caffe_navigate'))

        # check if WorkedHours has changed
        worked_hours = WorkedHours.objects.get(pk=self.worked_hours_main.pk)
        self.assertEqual(worked_hours.start_time, time(21, 0))
        self.assertEqual(worked_hours.end_time, time(22, 0))
        self.assertEqual(worked_hours.date, date(2016, 5, 31))
        self.assertEqual(worked_hours.position, self.barista)
        self.assertEqual(worked_hours.employee, self.user)

    def test_edit_workedhours_post_success(self):
        """Check if edit WorkedHours successes to edit when form is valid."""

        response = self.client.post(
            reverse('edit_worked_hours', args=(self.worked_hours_main.pk,)),
            {
                'start_time': '21:00',
                'end_time': '22:00',
                'date': '31.05.2016',
                'position': self.barista.id
            },
            follow=True
        )

        self.assertRedirects(response, reverse('caffe_navigate'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, "success")
        self.assertTrue("poprawnie" in messages[0].message)

        # check if WorkedHours has changed
        worked_hours = WorkedHours.objects.get(pk=self.worked_hours_main.pk)
        self.assertEqual(worked_hours.start_time, time(21, 0))
        self.assertEqual(worked_hours.end_time, time(22, 0))
        self.assertEqual(worked_hours.date, date(2016, 5, 31))
        self.assertEqual(worked_hours.position, self.barista)
        self.assertEqual(worked_hours.employee, self.user)
