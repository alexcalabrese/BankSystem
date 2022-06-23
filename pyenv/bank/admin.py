from django.contrib import admin
from .models.account import Account
from .models.transaction import Transaction
from .models.transaction import SelfTransaction

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(SelfTransaction)
