
from tkinter import CASCADE
from unicodedata import name
import uuid
from django.db import models
from .utils import create_random_string_id


class Account(models.Model):
    id = models.CharField(max_length=20, primary_key=True,
                          default=create_random_string_id, editable=False)
    name = models.CharField(max_length=50, unique=False)
    surname = models.CharField(max_length=50, unique=False)
    balance = models.FloatField(default=0, editable=False)

    def __str__(self):
        return self.name + self.surname


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)
    account_from = models.ForeignKey(
        Account, related_name='account_from', null=True, on_delete=models.CASCADE)
    account_to = models.ForeignKey(
        Account, related_name='account_to', null=True, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)
