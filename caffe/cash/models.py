"""Module with all models related to cash reports."""

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    """Stores one company a cafe interacts with (e.g., GoodCake bakery)."""

    name = models.CharField(max_length=200)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'caffe',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def save(self, *args, **kwargs):
        """Save model into the database."""

        self.full_clean()
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Expense(models.Model):
    """Represents an object a cafe pays for during the day (e.g., cakes).

    One entry could look like this:
    (name: cakes, company: GoodCake) or
    (name: newspapers).
    """

    name = models.CharField(max_length=300)
    company = models.ForeignKey('Company', blank=True, null=True)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('name', 'company')
        default_permissions = ('add', 'change', 'delete', 'view')

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        # checks if there exists two products with same name
        query = Expense.objects.filter(name=self.name, caffe=self.caffe)
        if self.pk:
            query = query.exclude(pk=self.pk)

        if query.exists():
            raise ValidationError(
                _('Wydatek powinien mieć unikalną nazwę.')
            )

        super(Expense, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        if self.company:
            if self.caffe != self.company.caffe:
                raise ValidationError(
                    _('Kawiarnia i kawiarnia firmy nie zgadza się.')
                )

        self.full_clean()
        super(Expense, self).save(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.name, self.company)


class FullExpense(models.Model):
    """Stores one specific expense - expense and amount.

    Is assigned to one report and can't be reused.
    """

    expense = models.ForeignKey('Expense')
    amount = models.FloatField()
    cash_report = models.ForeignKey(
        'CashReport',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='full_expenses'
    )
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        # checks if there exists two same expenses
        full_expenses = []
        if self.cash_report is not None:
            full_expenses = self.cash_report.full_expenses.all()

        for full_expense in full_expenses:
            if full_expense.expense == self.expense:
                raise ValidationError(
                    _('Cash Report should not contain two same expenses.')
                )

        super(FullExpense, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        if self.cash_report:
            if self.caffe != self.cash_report.caffe:
                raise ValidationError(
                    _('Kawiarnia i kawiarnia raportu z kasy nie zgadza się.')
                )

        if self.caffe != self.expense.caffe:
            raise ValidationError(
                _('Kawiarnia i kawiarnia wydatku nie zgadza się.')
            )

        self.full_clean()
        super(FullExpense, self).save(*args, **kwargs)

    def __str__(self):
        return '{}: {}'.format(self.expense, self.amount)


class CashReport(models.Model):
    """Stores a single report representing money flow during one shift."""

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('employees.Employee')
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    cash_before_shift = models.FloatField()
    cash_after_shift = models.FloatField()
    card_payments = models.FloatField()
    amount_due = models.FloatField()

    class Meta:
        ordering = ('-created_on', '-updated_on')
        default_permissions = ('add', 'change', 'delete', 'view')

    def balance(self):
        """Calculate balance within one report, indicate deficit/surplus."""

        expenses = 0
        if self.full_expenses.count() > 0:
            expenses = (
                self.full_expenses.aggregate(Sum('amount'))['amount__sum']
            )

        return (self.cash_after_shift + self.card_payments + expenses - \
                self.cash_before_shift - self.amount_due)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        if self.creator is not None:
            if self.caffe != self.creator.caffe:
                raise ValidationError(
                    _('Kawiarnia i kawiarnia tworzącego powinna się zgadzać')
                )

        self.full_clean()
        super(CashReport, self).save(*args, **kwargs)

    def __str__(self):
        return 'Report created: {:%Y-%m-%d %H:%M} by {}'.format(
            self.created_on,
            self.creator
        )
