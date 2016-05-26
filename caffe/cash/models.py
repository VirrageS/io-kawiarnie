"""Module with all models related to cash reports."""

from django.db import models
from django.db.models import Sum

from employees.models import Employee


class CashReport(models.Model):
    """Stores a single report representing money flow during one shift."""

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(Employee)

    cash_before_shift = models.FloatField()
    cash_after_shift = models.FloatField()
    card_payments = models.FloatField()
    amount_due = models.FloatField()

    class Meta:
        ordering = ('-created_on', '-updated_on')
        default_permissions = ('add', 'change', 'delete', 'view')

    def balance(self):
        """Calculate balance within one report, indicate deficit/surplus."""

        expenses = self.full_expense.aggregate(Sum('amount'))['amount__sum']

        return self.cash_after_shift + self.card_payments + expenses -\
            self.cash_before_shift - self.amount_due

    def __str__(self):
        return 'Report created: {:%Y-%m-%d %H:%M} by {}'.format(
            self.created_on,
            self.creator
        )


class Company(models.Model):
    """Stores one company a cafe interacts with (e.g., GoodCake bakery)."""

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return '{}'.format(self.name)


class Expense(models.Model):
    """Represents an object a cafe pays for during the day (e.g., cakes).

    One entry could look like this:
    (name: cakes, company: GoodCake) or
    (name: newspapers).
    """

    name = models.CharField(max_length=300)
    company = models.ForeignKey(Company, blank=True, null=True)

    class Meta:
        ordering = ('name', 'company')
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return '{}, {}'.format(self.name, self.company)


class FullExpense(models.Model):
    """Stores one specific expense - expense and amount.

    Is assigned to one report and can't be reused.
    """

    expense = models.ForeignKey(Expense)
    amount = models.FloatField()
    cash_report = models.ForeignKey(
        CashReport,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='full_expense'
    )

    def __str__(self):
        return '{}: {}'.format(self.expense, self.amount)
