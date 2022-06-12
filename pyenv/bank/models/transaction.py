import uuid
from django.db import models
from .account import Account
from rest_framework.exceptions import NotFound


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)
    account_from = models.ForeignKey(
        Account, related_name='account_from', null=True, on_delete=models.SET_NULL)
    account_to = models.ForeignKey(
        Account, related_name='account_to', null=True, on_delete=models.SET_NULL)
    amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.id)


def get_transaction_if_exist(id):
    try:
        transaction = Transaction.objects.get(pk=id)
    except Exception:
        raise NotFound({"message": "Error 404, transaction not found"})
    return transaction
