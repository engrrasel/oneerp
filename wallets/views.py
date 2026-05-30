from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

from .models import Wallet
from transactions.models import Transaction

from .models import WalletTransfer

from django.db.models import Sum


from decimal import Decimal
from datetime import date

@login_required
def wallet_list(request):

    wallets = Wallet.objects.filter(
        user=request.user
    )

    for wallet in wallets:

        income = (
            Transaction.objects.filter(
                wallet=wallet,
                transaction_type='income',
                is_deleted=False
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        expense = (
            Transaction.objects.filter(
                wallet=wallet,
                transaction_type='expense',
                is_deleted=False
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        incoming_transfer = (
            WalletTransfer.objects.filter(
                to_wallet=wallet
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        outgoing_transfer = (
            WalletTransfer.objects.filter(
                from_wallet=wallet
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        wallet.current_balance = (
            wallet.opening_balance
            + income
            - expense
            + incoming_transfer
            - outgoing_transfer
        )

    return render(
        request,
        'wallets/wallet_list.html',
        {
            'active_tab': 'wallets',
            'wallets': wallets
        }
    )



@login_required
def wallet_add(request):

    if request.method == 'POST':

        Wallet.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            opening_balance=request.POST.get(
                'opening_balance'
            ) or 0
        )

        messages.success(
            request,
            'Wallet created successfully.'
        )

        return redirect(
            'wallet_list'
        )

    return render(
        request,
        'wallets/wallet_add.html',
        {
            'active_tab': 'wallets',
        }
    )
@login_required
def wallet_edit(request, pk):

    wallet = get_object_or_404(
        Wallet,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':

        wallet.name = request.POST.get(
            'name',
            ''
        ).strip()

        wallet.wallet_type = request.POST.get(
            'wallet_type',
            'cash'
        )

        wallet.opening_balance = (
            request.POST.get(
                'opening_balance'
            ) or 0
        )

        wallet.bank_name = request.POST.get(
            'bank_name',
            ''
        ).strip()

        wallet.branch_name = request.POST.get(
            'branch_name',
            ''
        ).strip()

        wallet.account_name = request.POST.get(
            'account_name',
            ''
        ).strip()

        wallet.account_number = request.POST.get(
            'account_number',
            ''
        ).strip()

        wallet.mobile_number = request.POST.get(
            'mobile_number',
            ''
        ).strip()

        wallet.save()

        messages.success(
            request,
            'Wallet updated successfully.'
        )

        return redirect(
            'wallet_list'
        )

    return render(
        request,
        'wallets/wallet_edit.html',
        {
            'active_tab': 'wallets',
            'wallet': wallet
        }
    )

@login_required
def wallet_delete(request, pk):

    wallet = get_object_or_404(
        Wallet,
        pk=pk,
        user=request.user
    )

    wallet.delete()

    messages.success(
        request,
        'Wallet deleted successfully.'
    )

    return redirect(
        'wallet_list'
    )


@login_required
def wallet_detail(request, pk):

    wallet = get_object_or_404(
        Wallet,
        pk=pk,
        user=request.user
    )

    transactions = (
        Transaction.objects
        .filter(
            wallet=wallet,
            is_deleted=False
        )
        .select_related(
            'category'
        )
    )

    start_date = request.GET.get(
        'start_date'
    )

    end_date = request.GET.get(
        'end_date'
    )

    transaction_type = request.GET.get(
        'type'
    )

    search = request.GET.get(
        'search'
    )

    if start_date:

        transactions = transactions.filter(
            transaction_date__gte=start_date
        )

    if end_date:

        transactions = transactions.filter(
            transaction_date__lte=end_date
        )

    if transaction_type:

        transactions = transactions.filter(
            transaction_type=transaction_type
        )

    if search:

        transactions = transactions.filter(
            note__icontains=search
        )

    transactions = transactions.order_by(
        '-transaction_date',
        '-id'
    )

    total_income = (
        transactions
        .filter(
            transaction_type='income'
        )
        .aggregate(
            total=models.Sum('amount')
        )['total']
        or 0
    )

    total_expense = (
        transactions
        .filter(
            transaction_type='expense'
        )
        .aggregate(
            total=models.Sum('amount')
        )['total']
        or 0
    )

    incoming_transfer = (
        WalletTransfer.objects.filter(
            to_wallet=wallet
        ).aggregate(
            total=models.Sum('amount')
        )['total']
        or 0
    )

    outgoing_transfer = (
        WalletTransfer.objects.filter(
            from_wallet=wallet
        ).aggregate(
            total=models.Sum('amount')
        )['total']
        or 0
    )

    current_balance = (
        wallet.opening_balance
        + total_income
        - total_expense
        + incoming_transfer
        - outgoing_transfer
    )

    transfers_out = (
        WalletTransfer.objects
        .filter(
            from_wallet=wallet
        )
        .select_related(
            'to_wallet'
        )
        .order_by(
            '-transfer_date',
            '-id'
        )
    )

    transfers_in = (
        WalletTransfer.objects
        .filter(
            to_wallet=wallet
        )
        .select_related(
            'from_wallet'
        )
        .order_by(
            '-transfer_date',
            '-id'
        )
    )
    return render(
        request,
        'wallets/wallet_detail.html',
        {
            'active_tab': 'wallets',
            'wallet': wallet,
            'transactions': transactions,
            'total_income': total_income,
            'total_expense': total_expense,
            'incoming_transfer': incoming_transfer,
            'outgoing_transfer': outgoing_transfer,
            'current_balance': current_balance,
            'transfers_out': transfers_out,
            'transfers_in': transfers_in,
        }
    )


@login_required
def transfer_add(request):

    wallets = Wallet.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        send_from = Wallet.objects.get(
            id=request.POST.get('send_from'),
            user=request.user
        )

        send_to = Wallet.objects.get(
            id=request.POST.get('send_to'),
            user=request.user
        )

        amount = Decimal(
            request.POST.get('amount')
        )

        if send_from == send_to:

            messages.error(
                request,
                'Source and destination wallet cannot be same.'
            )

            return redirect(
                'wallet_list'
            )

        income = (
            Transaction.objects.filter(
                wallet=send_from,
                transaction_type='income',
                is_deleted=False
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        expense = (
            Transaction.objects.filter(
                wallet=send_from,
                transaction_type='expense',
                is_deleted=False
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        incoming_transfer = (
            WalletTransfer.objects.filter(
                to_wallet=send_from
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        outgoing_transfer = (
            WalletTransfer.objects.filter(
                from_wallet=send_from
            ).aggregate(
                total=Sum('amount')
            )['total']
            or 0
        )

        current_balance = (
            send_from.opening_balance
            + income
            - expense
            + incoming_transfer
            - outgoing_transfer
        )

        if amount > current_balance:

            messages.error(
                request,
                'Insufficient balance.'
            )

            return redirect(
                'wallet_list'
            )

        WalletTransfer.objects.create(

            user=request.user,

            from_wallet=send_from,

            to_wallet=send_to,

            amount=amount,

            note=request.POST.get(
                'note',
                ''
            ),

            transfer_date=date.today()
            )
        

        messages.success(
            request,
            'Transfer completed successfully.'
        )

        return redirect(
            'wallet_list'
        )

    return redirect(
        'wallet_list'
    )