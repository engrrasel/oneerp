from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Wallet(models.Model):

    WALLET_TYPES = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('mobile_banking', 'Mobile Banking'),
        ('card', 'Card'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wallets'
    )

    name = models.CharField(
        max_length=100
    )

    wallet_type = models.CharField(
        max_length=20,
        choices=WALLET_TYPES,
        default='cash'
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    bank_name = models.CharField(
        max_length=100,
        blank=True
    )

    branch_name = models.CharField(
        max_length=100,
        blank=True
    )

    account_name = models.CharField(
        max_length=150,
        blank=True
    )

    account_number = models.CharField(
        max_length=100,
        blank=True
    )

    routing_number = models.CharField(
        max_length=50,
        blank=True
    )

    mobile_number = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.name


class WalletTransfer(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    from_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name='outgoing_transfers'
    )

    to_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name='incoming_transfers'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    note = models.TextField(
        blank=True
    )

    transfer_date = models.DateField(
        default=timezone.now
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            '-transfer_date',
            '-id'
        ]

    def __str__(self):

        return (
            f'{self.from_wallet} → '
            f'{self.to_wallet}'
        )