from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from transactions.models import Transaction


@login_required
def dashboard_view(request):

    transactions = Transaction.objects.filter(
        user=request.user,
        is_deleted=False
    )

    income_total = (
        transactions
        .filter(transaction_type='income')
        .aggregate(total=Sum('amount'))
        .get('total')
        or 0
    )

    expense_total = (
        transactions
        .filter(transaction_type='expense')
        .aggregate(total=Sum('amount'))
        .get('total')
        or 0
    )

    balance = income_total - expense_total

    recent_transactions = transactions[:10]

    context = {

        'income_total': income_total,

        'expense_total': expense_total,

        'balance': balance,

        'recent_transactions': recent_transactions,

        'transaction_count': transactions.count(),

    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )