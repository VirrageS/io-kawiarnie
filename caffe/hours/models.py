from django.db import models

import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.

class WorkedHours(models.Model):
    """Stores one period of worked hours by one employee."""

    employee = models.ForeignKey(
        'employees.Employee',
        unique=False,
        null=True,
        blank=True,
        default=None
    )

    start_time = models.TimeField(auto_now=False)
    end_time = models.TimeField(auto_now=False)
    date =  models.DateField(auto_now=False)


    class Meta:
        ordering = ('-date', 'end_time')
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return 'Worked hours: {} {} {} {}'.format(
            self.employee,
            self.start_time,
            self.end_time,
            self.date
        )

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""
        intersect = []
        intersect = \
            WorkedHours.objects.filter(
                employee=self.employee,
                date=self.date,
                start_time__lte=self.end_time,
                end_time__gte=self.start_time
            )

        if intersect.count() > 0:
            raise ValidationError(
                'Such working hours already exist for this employee'
            )
