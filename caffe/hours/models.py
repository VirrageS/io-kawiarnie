from django.db import models


from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.

class WorkedHours(models.models):
    """Stores one period of worked hours by one employee."""

    employee = models.ForeginKey(
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
        return 'Worked hours: {} {%H:%M} {%H:%M} {}'.format(
            self.employee,
            self.start_time,
            self.end_time,
            self.date
        )