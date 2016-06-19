import json

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CashReportForm, CompanyForm, ExpenseForm, FullExpenseForm
from .models import CashReport, Company, Expense, FullExpense


@permission_required('cash.add_company')
def cash_new_company(request):
    """Show form to create new Company and show existing Companies."""

    elements = []

    form = CompanyForm(request.POST or None, caffe=request.user.caffe)

    if form.is_valid():
        form.save()
        messages.success(request, 'Firma została poprawnie dodana.')

        return redirect(reverse('cash_navigate'))

    companies = Company.objects.filter(caffe=request.user.caffe).all()
    for company in companies:
        elements.append({
            'edit_href': reverse('cash_edit_company', args=(company.id,)),
            'id': company.id,
            'desc': str(company)
        })

    return render(request, 'cash/new_element.html', {
        'form': form,
        'context': {
            'title': u'Nowa firma'
        },
        'elements': elements
    })


@permission_required('cash.change_company')
def cash_edit_company(request, company_id):
    """Show form to edit Company.

    Args:
        company_id (int): Id of Company which is edited.
    """

    company = get_object_or_404(
        Company,
        id=company_id,
        caffe=request.user.caffe
    )

    form = CompanyForm(
        request.POST or None,
        caffe=request.user.caffe,
        instance=company
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Firma została poprawnie zmieniona.')
        return redirect(reverse('cash_navigate'))

    return render(request, 'cash/edit_element.html', {
        'form': form,
        'context': {
            'title': u'Edytuj firmę',
            'cancel_href': reverse('cash_new_company')
        }
    })


@permission_required('cash.add_expense')
def cash_new_expense(request):
    """Show form to create new Expense and show already existing Expenses."""

    elements = []
    form = ExpenseForm(request.POST or None, caffe=request.user.caffe)

    if form.is_valid():
        form.save()
        messages.success(request, 'Wydatek został poprawnie dodany.')
        return redirect(reverse('cash_navigate'))

    expenses = Expense.objects.filter(caffe=request.user.caffe).all()
    for expense in expenses:
        elements.append({
            'edit_href': reverse('cash_edit_expense', args=(expense.id,)),
            'id': expense.id,
            'desc': str(expense)
        })

    return render(request, 'cash/new_element.html', {
        'form': form,
        'context': {
            'title': "Nowy wydatek"
        },
        'elements': elements
    })


@permission_required('cash.change_expense')
def cash_edit_expense(request, expense_id):
    """Show form to edit Expense.

    Args:
        expense_id (int): Id of Expense which is edited.
    """

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        caffe=request.user.caffe
    )

    form = ExpenseForm(
        request.POST or None,
        caffe=request.user.caffe,
        instance=expense
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Wydatek został poprawnie zmieniony.')
        return redirect(reverse('cash_navigate'))

    return render(request, 'cash/edit_element.html', {
        'form': form,
        'context': {
            'title': 'Edytuj wydatek',
            'cancel_href': reverse('cash_new_expense')
        }
    })


@permission_required('cash.add_cashreport')
def cash_new_cash_report(request):
    """Show form to create CashReport and show already existing CashReport."""

    all_expenses = []
    form = CashReportForm(
        request.POST or None,
        caffe=request.user.caffe,
        creator=request.user
    )

    for expense in Expense.objects.filter(caffe=request.user.caffe).all():
        all_expenses.append({
            'id': expense.id,
            'name': expense.name,
            'selected': False,
            'amount': 0,
            'errors': {}
        })

        if expense.company:
            all_expenses[-1]['company'] = {
                'id': expense.company.id,
                'name': expense.company.name,
            }

    if request.POST:
        forms = []
        valid = form.is_valid()

        for full_expense in request.POST:
            fe_list = []

            try:
                full_expense = int(full_expense)
                fe_list = request.POST.getlist(str(full_expense))
            except ValueError:
                continue

            if len(fe_list) != 2:
                continue

            expense_form = FullExpenseForm(
                {'expense': fe_list[0], 'amount': fe_list[1]},
                caffe=request.user.caffe
            )

            valid = valid & expense_form.is_valid()

            expense = next(
                (e for e in all_expenses if e['id'] == int(fe_list[0])),
                None
            )

            if expense:
                expense['selected'] = True

                if expense_form.is_valid():
                    expense['amount'] = fe_list[1]
                    expense['errors'] = ''
                else:
                    expense['amount'] = ''
                    expense['errors'] = expense_form.errors.get('amount')

            forms.append(expense_form)

        if valid:
            cash_report = form.save()

            for form in forms:
                full_expense = form.save()
                full_expense.cash_report = cash_report
                full_expense.save()

            cash_report.save()
            messages.success(request, 'Raport z kasy został poprawnie dodany.')
            return redirect(reverse('cash_navigate'))
        else:
            messages.error(
                request, u'Formularz został niepoprawnie wypełniony.'
            )

    return render(request, 'cash/new_report.html', {
        'title':  'Nowy raport z kasy',
        'button': 'Dodaj',
        'form': form,
        'expenses': json.dumps(all_expenses),
    })


@permission_required('cash.change_cashreport')
def cash_edit_cash_report(request, report_id):
    """Show form to edit CashReport.

    Args:
        report_id (int): Id of CashReport which is edited.
    """

    cash_report = get_object_or_404(
        CashReport,
        id=report_id,
        caffe=request.user.caffe
    )

    form = CashReportForm(
        request.POST or None,
        caffe=request.user.caffe,
        creator=request.user,
        instance=cash_report
    )

    all_expenses = []
    for expense in Expense.objects.filter(caffe=request.user.caffe).all():
        all_expenses.append({
            'id': expense.id,
            'name': expense.name,
            'selected': False,
            'amount': 0,
            'errors': {}
        })

        if expense.company:
            all_expenses[-1]['company'] = {
                'id': expense.company.id,
                'name': expense.company.name,
            }

        full_expense = FullExpense.objects.filter(
            cash_report=cash_report.id, expense=expense.id
        ).first()

        if full_expense and (not request.POST):
            all_expenses[-1]['selected'] = True
            all_expenses[-1]['amount'] = full_expense.amount

    if request.POST:
        forms = []
        valid = form.is_valid()

        for full_expense in request.POST:
            fe_list = []

            try:
                full_expense = int(full_expense)
                fe_list = request.POST.getlist(str(full_expense))
            except ValueError:
                continue

            if len(fe_list) != 2:
                continue

            expense_form = FullExpenseForm(
                {'expense': fe_list[0], 'amount': fe_list[1]},
                caffe=request.user.caffe
            )

            valid = valid & expense_form.is_valid()

            expense = next(
                (e for e in all_expenses if e['id'] == int(fe_list[0])),
                None
            )

            if expense:
                expense['selected'] = True
                if expense_form.is_valid():
                    expense['amount'] = fe_list[1]
                    expense['errors'] = ''
                else:
                    expense['amount'] = ''
                    expense['errors'] = expense_form.errors.get('amount')

            forms.append(expense_form)

        if valid:
            cash_report = form.save()

            for full_expense in cash_report.full_expenses.all():
                full_expense.delete()

            for form in forms:
                full_expense = form.save()
                full_expense.cash_report = cash_report
                full_expense.save()

            cash_report.save()
            messages.success(
                request, 'Raport z kasy został poprawnie zmieniony.'
            )

            return redirect(reverse('cash_navigate'))
        else:
            messages.error(
                request, u'Formularz został niepoprawnie wypełniony.'
            )

    return render(request, 'cash/new_report.html', {
        'title':  'Nowy raport z kasy',
        'button': 'Uaktualnij',
        'form': form,
        'expenses': json.dumps(all_expenses),
    })


@permission_required('cash.view_cashreport')
def cash_show_cash_report(request, report_id):
    """Show CashReport with all Expenses.

    Args:
        report_id (int): Id of CashReport which have to be shown.
    """

    cash_report = get_object_or_404(
        CashReport,
        id=report_id,
        caffe=request.user.caffe
    )
    cash_report.balance = cash_report.balance()

    all_expenses = []
    for full_expense in cash_report.full_expenses.all():
        all_expenses.append({
            'name': full_expense.expense.name,
            'amount': full_expense.amount
        })

    return render(request, 'cash/show.html', {
        'report': cash_report,
        'expenses': all_expenses
    })


def cash_navigate(request):
    """Show navigation view for CashReport."""

    return render(request, 'home/cash.html')
