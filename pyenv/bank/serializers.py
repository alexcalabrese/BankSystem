from rest_framework import serializers
from .models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id',
                  'account_from',
                  'account_to',
                  'amount']


class AccountSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(
        source='account_from',
        queryset=Transaction.objects.order_by('created_at'),
        many=True)

    class Meta:
        model = Account
        fields = ['id',
                  'name',
                  'surname',
                  'balance',
                  'transactions']
