from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


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

        same_position = Position.objects.filter(
            name__iexact=self.name,
            caffe=self.caffe
        )

        if self.pk:
            same_position = same_position.exclude(pk=self.pk)

        if same_position.exists():
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
        'employees.Employee',
        null=True,
        blank=False,
        default=None
    )
    position = models.ForeignKey(
        'Position',
        null=True,
        blank=False,
        default=None
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

    def save(self, *args, **kwargs):
        """Save model into the database."""

        if self.employee:
            if self.caffe != self.employee.caffe:
                raise ValidationError(
                    _('Kawiarnia i kawiarnia pracownika nie zgadza się.')
                )

        if self.caffe != self.position.caffe:
            raise ValidationError(
                _('Kawiarnia i kawiarnia stanowiska nie zgadza się.')
            )

        self.full_clean()
        super(WorkedHours, self).save(*args, **kwargs)

    def __str__(self):
        return 'Worked hours: {} {} {} {}'.format(
            self.employee,
            self.start_time,
            self.end_time,
            self.date
        )
