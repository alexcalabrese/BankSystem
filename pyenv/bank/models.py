
from unicodedata import name
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
