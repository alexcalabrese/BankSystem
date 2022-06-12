from django.db import models
from ..utils import create_random_string_id
from rest_framework.exceptions import NotFound


class Account(models.Model):
    id = models.CharField(max_length=20, primary_key=True,
                          default=create_random_string_id, editable=False)
    name = models.CharField(max_length=50, unique=False)
    surname = models.CharField(max_length=50, unique=False)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.name + " " + self.surname

    def deposit(self, amount):
        previus_balance = self.balance
        self.balance = previus_balance + amount
        self.save()

    def withdrawal(self, amount):
        previus_balance = self.balance
        self.balance = previus_balance - amount
        self.save()


def get_account_if_exist(id):
    try:
        account = Account.objects.get(pk=id)
        return account
    except Account.DoesNotExist:
        raise NotFound({"message": "Error 404, account not found"})
