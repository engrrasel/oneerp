from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)


from wallets.models import Wallet
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.exceptions import ValidationError

from django.db import transaction as db_transaction

from expenses.models import Category


from .models import (
    Transaction,
    TransactionHistory,
    AuditLog
)


@login_required
def transaction_list(request):

    transactions = (
        Transaction.objects
        .select_related('category')
        .filter(
            user=request.user,
            is_deleted=False
        )
    )

    return render(
        request,
        'transactions/transaction_list.html',
        {
            'active_tab': 'transactions',
            'transactions': transactions
        }
    )


@login_required
def deleted_transactions(request):

    transactions = (
        Transaction.objects
        .select_related('category')
        .filter(
            user=request.user,
            is_deleted=True
        )
    )

    return render(
        request,
        'transactions/deleted_transactions.html',
        {
            'active_tab': 'transactions',
            'transactions': transactions
        }
    )




@login_required
def transaction_add(request):

    categories = Category.objects.filter(
        user=request.user
    )

    wallets = Wallet.objects.filter(
        user=request.user,
        is_active=True
    )

    if request.method == 'POST':

        try:

            with db_transaction.atomic():

                transaction = Transaction(

                    user=request.user,

                    created_by=request.user,

                    category_id=request.POST.get(
                        'category'
                    ),

                    wallet_id=request.POST.get(
                        'wallet'
                    ),

                    transaction_type=request.POST.get(
                        'transaction_type'
                    ),

                    amount=request.POST.get(
                        'amount'
                    ),

                    note=request.POST.get(
                        'note'
                    ),

                    transaction_date=request.POST.get(
                        'transaction_date'
                    )
                )

                transaction.save()

                AuditLog.objects.create(

                    user=request.user,

                    action='create',

                    transaction=transaction,

                    description=f'Created transaction #{transaction.id}'
                )

            messages.success(
                request,
                'Transaction added successfully.'
            )

            return redirect(
                'transaction_list'
            )

        except ValidationError as e:

            if hasattr(e, 'message_dict'):

                for errors in e.message_dict.values():

                    for error in errors:

                        messages.error(
                            request,
                            error
                        )

            else:

                messages.error(
                    request,
                    str(e)
                )

        except Exception as e:

            messages.error(
                request,
                str(e)
            )

    return render(
        request,
        'transactions/transaction_add.html',
        {
            'active_tab': 'transactions',
            'categories': categories,
            'wallets': wallets,
        }
    )


@login_required
def transaction_edit(request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user,
        is_deleted=False
    )

    categories = Category.objects.filter(
        user=request.user
    )

    wallets = Wallet.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        try:

            with db_transaction.atomic():

                old_amount = transaction.amount

                old_category_name = (
                    transaction.category.name
                )

                old_transaction_type = (
                    transaction.transaction_type
                )

                old_note = transaction.note

                old_transaction_date = (
                    transaction.transaction_date
                )

                transaction.category_id = request.POST.get(
                    'category'
                )

                transaction.wallet_id = request.POST.get(
                    'wallet'
                )

                transaction.transaction_type = request.POST.get(
                    'transaction_type'
                )

                transaction.amount = request.POST.get(
                    'amount'
                )

                transaction.note = request.POST.get(
                    'note'
                )

                transaction.transaction_date = request.POST.get(
                    'transaction_date'
                )

                transaction.updated_by = request.user

                transaction.save()

                TransactionHistory.objects.create(

                    transaction=transaction,

                    changed_by=request.user,

                    amount=old_amount,

                    category_name=old_category_name,

                    transaction_type=old_transaction_type,

                    note=old_note,

                    transaction_date=old_transaction_date
                )

                AuditLog.objects.create(

                    user=request.user,

                    action='update',

                    transaction=transaction,

                    description=f'Updated transaction #{transaction.id}'
                )

            messages.success(
                request,
                'Transaction updated successfully.'
            )

            return redirect(
                'transaction_list'
            )

        except ValidationError as e:

            if hasattr(e, 'message_dict'):

                for errors in e.message_dict.values():

                    for error in errors:

                        messages.error(
                            request,
                            error
                        )

            else:

                messages.error(
                    request,
                    str(e)
                )

        except Exception as e:

            messages.error(
                request,
                str(e)
            )

    return render(
        request,
        'transactions/transaction_edit.html',
        {
            'active_tab': 'transactions',
            'transaction': transaction,
            'categories': categories,
            'wallets': wallets,
        }
    )


@login_required
def transaction_delete(request, pk):

    try:

        transaction = get_object_or_404(

            Transaction,

            pk=pk,

            user=request.user,

            is_deleted=False
        )

        with db_transaction.atomic():

            transaction.soft_delete(
                request.user
            )

            AuditLog.objects.create(

                user=request.user,

                action='delete',

                transaction=transaction,

                description=
                f'Deleted transaction #{transaction.id}'
            )

        messages.success(
            request,
            'Transaction moved to trash.'
        )

    except Exception as e:

        messages.error(
            request,
            f'Error: {str(e)}'
        )

    return redirect(
        'transaction_list'
    )


@login_required
def transaction_restore(request, pk):

    try:

        transaction = get_object_or_404(

            Transaction,

            pk=pk,

            user=request.user,

            is_deleted=True
        )

        with db_transaction.atomic():

            transaction.restore()

            AuditLog.objects.create(

                user=request.user,

                action='restore',

                transaction=transaction,

                description=
                f'Restored transaction #{transaction.id}'
            )

        messages.success(
            request,
            'Transaction restored successfully.'
        )

    except Exception as e:

        messages.error(
            request,
            f'Error: {str(e)}'
        )

    return redirect(
        'deleted_transactions'
    )


@login_required
def transaction_history(request, pk):

    transaction = get_object_or_404(

        Transaction,

        pk=pk,

        user=request.user
    )

    histories = (
        transaction.histories
        .select_related('changed_by')
        .all()
    )

    return render(
        request,
        'transactions/transaction_history.html',
        {
            'active_tab': 'transactions',
            'transaction': transaction,
            'histories': histories
        }
    )