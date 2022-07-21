import uuid
from django.db import models

from bank.utils import is_valid_uuid

from .selfTransansaction import SelfTransaction
from .account import Account
from rest_framework.exceptions import NotFound, ValidationError


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)
    account_from = models.ForeignKey(
        Account, related_name='account_from', null=True, on_delete=models.DO_NOTHING)
    account_to = models.ForeignKey(
        Account, related_name='account_to', null=True, on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    is_diverted = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.id)


def get_transaction_if_exist(id):
    if not is_valid_uuid(id):
        raise ValidationError(
            {"message": "Error 400, id is not valid"})

    if SelfTransaction.objects.filter(pk=id).exists():
        raise ValidationError(
            {"message": "Error 400, cannot divert a Deposit/Withdrawal"})

    try:
        transaction = Transaction.objects.get(pk=id)

        if transaction.is_diverted:
            raise ValidationError(
                {"message": "Error 400, transaction is already diverted"})
        else:
            transaction = Transaction.objects.get(pk=id, is_diverted=0)
    except Transaction.DoesNotExist:
        raise NotFound({"message": "Error 404, transaction not found"})
    return transaction
