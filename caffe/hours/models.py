from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models


class WorkedHours(models.Model):
    """Stores one period of worked hours by one employee."""

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    employee = models.ForeignKey(
        'employees.Employee',
        unique=False,
        null=True,
        blank=True,
        default=None
    )

    start_time = models.TimeField(auto_now=False)
    end_time = models.TimeField(auto_now=False)
    date = models.DateField(auto_now=False)

    class Meta:
        ordering = ('-date', '-end_time')
        default_permissions = ('add', 'change', 'delete', 'view')

    def serialize(self):
        """Serialize model to dictionary.

        Returns:
            Dictionary with all neccessary informations about model.
        """

        employee = {}
        if self.employee:
            employee = {
                'id': self.employee.id,
                'first_name': self.employee.first_name
            }

        return {
            'id': self.id,
            'employee': employee,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'date': self.date,
            'url': reverse('get_worked_hours', args=(self.id,)),
            'edit_url': reverse('edit_worked_hours', args=(self.id,)),
        }

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        intersect = WorkedHours.objects.filter(
            employee=self.employee,
            date=self.date,
            start_time__lte=self.end_time,
            end_time__gte=self.start_time
        )

        if intersect.count() > 0:
            raise ValidationError(
                'Such working hours already exist for this employee'
            )

        if self.start_time > self.end_time:
            raise ValidationError(
                'Start time must be after end time'
            )

    def __str__(self):
        return 'Worked hours: {} {} {} {}'.format(
            self.employee,
            self.start_time,
            self.end_time,
            self.date
        )
