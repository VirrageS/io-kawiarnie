from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CashReportForm, CompanyForm, ExpenseForm
from .models import CashReport, Company, Expense


def cash_new_company(request):
    """Show form to create new Company and show existing Companies."""

    elements = []
    form = CompanyForm()

    if request.POST:
        form = CompanyForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('cash_navigate'))

    companies = Company.objects.all()
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


def cash_edit_company(request, company_id):
    """Show form to edit Company.

    Args:
        company_id (int): Id of Company which is edited.
    """

    company = get_object_or_404(Company, id=company_id)
    form = CompanyForm(request.POST or None, instance=company)

    if form.is_valid():
        form.save()
        return redirect(reverse('cash_navigate'))

    return render(request, 'cash/edit_element.html', {
        'form': form,
        'context': {
            'title': u'Edytuj firmę',
            'cancel_href': reverse('cash_new_company')
        }
    })


def cash_new_expense(request):
    """Show form to create new Expense and show already existing Expenses."""

    elements = []
    form = ExpenseForm()

    if request.POST:
        form = ExpenseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('cash_navigate'))

    expenses = Expense.objects.all()
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


def cash_edit_expense(request, expense_id):
    """Show form to edit Expense.

    Args:
        expense_id (int): Id of Expense which is edited.
    """

    expense = get_object_or_404(Expense, id=expense_id)
    form = ExpenseForm(request.POST or None, instance=expense)

    if form.is_valid():
        form.save()
        return redirect(reverse('cash_navigate'))

    return render(request, 'cash/edit_element.html', {
        'form': form,
        'context': {
            'title': 'Edytuj wydatek',
            'cancel_href': reverse('cash_new_expense')
        }
    })


def cash_new_cash_report(request):
    """Show form to create new CashReport and show already existing CashReport."""

    form = CashReportForm()

    if request.POST:
        form = CashReportForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('cash_navigate'))

    # get last five reports
    latest_reports = CashReport.objects.all()[:5]

    return render(request, 'cash/new_report.html', {
        'title':  'Nowy raport z kasy',
        'button': 'Dodaj',
        'form': form,
        'reports': latest_reports,
    })


def cash_edit_cash_report(request, report_id):
    """Show form to edit CashReport.

    Args:
        report_id (int): Id of CashReport which is edited.
    """

    report = get_object_or_404(Expense, id=expense_id)
    form = CashReportForm(request.POST or None, instance=report)

    if form.is_valid():
        form.save()
        return redirect(reverse('cash_navigate'))

    return render(request, 'cash/new_report.html', {
        'title': 'Edytuj raport z kasy',
        'button': 'Uaktulanij',
        'form': form
    })


def cash_show_cash_report(request, report_id):
    """Show CashReport with all Expenses.

    Args:
        report_id (int): Id of CashReport which have to be shown.
    """

    report = get_object_or_404(CashReport, id=report_id)

    return render(request, 'cash/show.html', {
        'report': report,
    })


def cash_show_all_cash_reports(request):
    """Show all existing CashReport."""

    reports = CashReport.objects.all()
    return render(request, 'cash/all.html', {'reports': reports})


def cash_navigate(request):
    """Show navigation view for CashReport."""

    return render(request, 'home/cash.html')
