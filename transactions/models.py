from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from expenses.models import Category
from wallets.models import Wallet


class Transaction(models.Model):

    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions'
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    note = models.TextField(
        blank=True,
        null=True
    )

    transaction_date = models.DateField()

    # Audit Fields

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_transactions'
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_transactions'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # Soft Delete

    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_transactions'
    )

    class Meta:
        ordering = [
            '-transaction_date',
            '-id'
        ]

    def clean(self):

        if not self.category_id:
            raise ValidationError(
                {'category': 'Please select a category.'}
            )

        if not self.wallet_id:
            raise ValidationError(
                {'wallet': 'Please select a wallet.'}
            )

        if self.category.user != self.user:
            raise ValidationError(
                {'category': 'Invalid category selected.'}
            )

        if self.wallet.user != self.user:
            raise ValidationError(
                {'wallet': 'Invalid wallet selected.'}
            )

        if self.amount is None:
            raise ValidationError(
                {'amount': 'Amount is required.'}
            )

        if self.amount <= 0:
            raise ValidationError(
                {'amount': 'Amount must be greater than zero.'}
            )

        if (
            self.transaction_date and
            self.transaction_date > timezone.now().date()
        ):
            raise ValidationError(
                {
                    'transaction_date':
                    'Future dates are not allowed.'
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(
            *args,
            **kwargs
        )

    def soft_delete(self, user=None):

        self.is_deleted = True

        self.deleted_at = timezone.now()

        self.deleted_by = user

        self.save()

    def restore(self):

        self.is_deleted = False

        self.deleted_at = None

        self.deleted_by = None

        self.save()

    def __str__(self):

        return (
            f"{self.get_transaction_type_display()} | "
            f"{self.wallet.name} | "
            f"{self.amount}"
        )


class TransactionHistory(models.Model):

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='histories'
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    category_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    transaction_type = models.CharField(
        max_length=10
    )

    note = models.TextField(
        blank=True,
        null=True
    )

    transaction_date = models.DateField()

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):

        return (
            f"History #{self.transaction_id}"
        )


class AuditLog(models.Model):

    ACTIONS = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('restore', 'Restore'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )

    action = models.CharField(
        max_length=20,
        choices=ACTIONS
    )

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):

        return (
            f"{self.action} - "
            f"{self.transaction_id}"
        )