from rest_framework import serializers

from bank.utils import validate_float_field
from .models.account import Account
from .models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id',
                  'account_from',
                  'account_to',
                  'amount']

    def validate(self, data):
        if data.get('account_from') is None:
            raise serializers.ValidationError(
                {"message": "Error 400, sender account is required"})
        elif data.get('account_to') is None:
            raise serializers.ValidationError(
                {"message": "Error 400, receiver account is required"})
        elif data.get('amount') is None:
            raise serializers.ValidationError(
                {"message": "Error 400, amount is required"})

        try:
            account_from = data.get('account_from')
            account_to = data.get('account_to')
        except serializers.NotFound:
            raise serializers.NotFound(
                {"message": "Error 404, account not found"})

        amount = validate_float_field(data.get('amount'), "amount")

        if account_from != account_to:
            if amount < 0:
                raise serializers.ValidationError(
                    {'message': 'Error 400, cannot perform negative transfer'})
            if abs(amount) >= abs(account_from.balance):
                raise serializers.ValidationError(
                    {'message': 'Error 400, not enough money',
                        'current_balance: ': account_from.balance})
        return data


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(
        source='account_from',
        many=True)

    class Meta:
        model = Account
        fields = ['id',
                  'name',
                  'surname',
                  'balance',
                  'transactions']

    def validate_name(self, name):
        if name is None:
            raise serializers.ValidationError(
                {"message": "Error 400, name  is required"})
        else:
            return name

    def validate_surname(self, surname):
        if surname is None:
            raise serializers.ValidationError(
                {"message": "Error 400, surname is required"})
        else:
            return surname
