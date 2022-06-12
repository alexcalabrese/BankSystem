from django.http import JsonResponse
from .models.account import Account, get_account_if_exist
from .utils import validate_float_field
from .models.transaction import Transaction
from .serializers import AccountSerializer, TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, ParseError, NotFound


def set_name_surname_header(response, serializer):
    response['X-Sistema-Bancario'] = str(serializer['name'].value) + \
        ";" + str(serializer['surname'].value)

    return True


@api_view(['GET', 'POST'])
def account_list(request):

    # Return all accounts
    # Expected body parameters: none
    if request.method == 'GET':
        accounts = Account.objects.all()
        account_serializer = AccountSerializer(accounts, many=True)
        return JsonResponse(account_serializer.data, safe=False)

    # Create new account
    # Return id of created account
    # Expected body parameters:
    #   - name
    #   - surname
    if request.method == 'POST':
        new_account_serializer = AccountSerializer(data=request.data)
        if new_account_serializer.is_valid():
            new_account_serializer.save()
            return Response(new_account_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': new_account_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'HEAD'])
def account_detail(request, id):

    found_account = get_account_if_exist(id)

    # Return account's detail and his transactions (older firsts)
    # Add "X-Sistema-Bancario" header with following format: "name;surname"
    # Expected body parameters: none
    if request.method == 'GET':
        account_serializer = AccountSerializer(found_account)
        response = JsonResponse(account_serializer.data, safe=False)
        set_name_surname_header(response, account_serializer)

        return response

    # Make a self transaction using "amount" parameter
    # if amount > 0 -> Deposit
    # if amount < 0 -> Withdraw
    # Expected body parameters:
    #   - amount
    if request.method == 'POST':

        # It's a Self Deposit or Withdraw
        account_from = found_account
        account_to = found_account

        amount = validate_float_field(
            request.POST.get('amount', False), "amount")

        if(amount == False):
            raise ValidationError({"message": "Error 400, amount is required"})

        if amount < 0 and abs(amount) > abs(account_from.balance):
            raise ValidationError({"message": "Error 400, not enough money"})
        else:
            previus_balance = account_to.balance
            account_to.balance = (previus_balance + amount)
            account_to.save()

            self_transaction = Transaction.objects.create(
                account_from=account_from,
                account_to=account_to,
                amount=amount
            )
            transaction_serializer = TransactionSerializer(self_transaction)

            return Response({"transaction_id": transaction_serializer.data['id'],
                             "updated_balance": account_to.balance})

    # Overwrite "name" and "surname"
    # Expected body parameters:
    #   - name
    #   - surname
    if request.method == 'PUT':
        request_name = request.POST.get('name', False)
        request_surname = request.POST.get('surname', False)

        if request_name != False and request_surname != False:
            found_account.name = str(request_name)
            found_account.surname = str(request_surname)
            found_account.save()
        else:
            raise ParseError(
                {"message": "Error 400, either name and surname are required"})

        account_serializer = AccountSerializer(found_account)
        return Response(account_serializer.data)

    # Overwrite "name" or "surname"
    # Expected body parameters:
    #   - only one between name and surname
    if request.method == 'PATCH':
        request_name = request.POST.get('name', False)
        request_surname = request.POST.get('surname', False)

        if request_name != False:
            found_account.name = str(request_name)
            found_account.save()
        elif request_surname != False:
            found_account.surname = str(request_surname)
            found_account.save()
        else:
            raise ParseError(
                {"message": "Error 400, at least name or surname is required"})

        account_serializer = AccountSerializer(found_account)
        return Response(account_serializer.data)

    # Return empty response with
    # "X-Sistema-Bancario" header with following format: "name;surname"
    # Expected body parameters: none
    if request.method == 'HEAD':
        response = Response(status=status.HTTP_200_OK)
        account_serializer = AccountSerializer(found_account)
        set_name_surname_header(response, account_serializer)

        return response


@api_view(['POST'])
def new_transfer(request):

    # Make a new transaction using "amount" parameter
    # Expected body parameters:
    #   - account_from_id
    #   - account_to_id
    #   - amount
    if request.method == 'POST':

        account_from = get_account_if_exist(
            request.POST.get('account_from', False))
        account_to = get_account_if_exist(
            request.POST.get('account_to', False))

        new_transaction = TransactionSerializer(data=request.data)

        if new_transaction.is_valid(raise_exception=True):
            amount = new_transaction.validated_data.get('amount')
            account_from.withdrawal(amount)
            account_to.deposit(amount)
            new_transaction.save()

        response = {"transaction_id": new_transaction.data['id']}
        response["account_from"] = ({"account_from_id": account_from.id,
                                     "updated_balance": account_from.balance})
        response["account_to"] = ({"account_to_id": account_to.id,
                                   "updated_balance": account_to.balance})

        return Response(response)


@api_view(['POST'])
def new_divert(request):

    # Revert a transaction using "transaction_id" parameter
    # Expected body parameters:
    #   - transaction_id
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', False)

        try:
            transaction = Transaction.objects.get(pk=transaction_id)
        except Exception:
            raise NotFound(
                {'message': 'Error 404, transaction not found'})

        try:
            transaction_account_from = Account.objects.get(
                pk=transaction.account_from.id)
            transaction_account_to = Account.objects.get(
                pk=transaction.account_to.id)
        except Account.DoesNotExist:
            return Response({'message': 'Error 404, one of two account no longer exist'}, status=status.HTTP_404_NOT_FOUND)

        amount_to_revert = transaction.amount
        difference_between_amounts = transaction_account_to.balance - amount_to_revert

        if difference_between_amounts >= 0:
            transaction_account_from.deposit(amount_to_revert)
            transaction_account_to.withdrawal(amount_to_revert)

            new_transaction = Transaction.objects.create(
                account_from=transaction_account_to,
                account_to=transaction_account_from,
                amount=-amount_to_revert
            )

            new_transaction_serializer = TransactionSerializer(new_transaction)
        else:
            raise ValidationError(
                {'message': 'Error 400, Not enough money to divert'})

        return Response(new_transaction_serializer.data)
