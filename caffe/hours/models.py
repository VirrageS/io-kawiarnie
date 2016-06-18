from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from employees.models import Employee


class Position(models.Model):
    """Stores the Position on which Employee has been working."""

    name = models.CharField(max_length=100,)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        self.name = self.name.lstrip().rstrip()
        if self.name == '':
            raise ValidationError(_('Position name is not valid.'))

        same_position = Position.objects.filter(name__iexact=self.name,
                                                caffe=self.caffe).all()

        if same_position:
            raise ValidationError(_('Position with same name already exists.'))

        super(Position, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        self.full_clean()
        super(Position, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class WorkedHours(models.Model):
    """Stores one period of worked hours by one employee."""

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(
        Employee, null=True, blank=False, default=None
    )
    position = models.ForeignKey(
        'Position', null=True, blank=False, default=None
    )
    start_time = models.TimeField(auto_now=False)
    end_time = models.TimeField(auto_now=False)
    date = models.DateField(auto_now=False)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('-date', '-end_time')
        default_permissions = ('add', 'change', 'delete', 'view', 'change_all')

    def serialize(self):
        """Serialize model to dictionary.

        Returns:
            Dictionary with all necessary information about model.
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
            'caffe': self.caffe_id
        }

    def __str__(self):
        return 'Worked hours: {} {} {} {}'.format(
            self.employee,
            self.start_time,
            self.end_time,
            self.date
        )
