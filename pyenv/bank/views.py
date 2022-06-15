from django.http import JsonResponse
from .models.account import Account, get_account_if_exist
from .utils import validate_float_field
from .models.transaction import Transaction, get_transaction_if_exist
from .serializers import AccountSerializer, TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, ParseError, NotFound


def set_name_surname_header(response, serializer):
    response['X-Sistema-Bancario'] = str(serializer['name'].value) + \
        ";" + str(serializer['surname'].value)

    return True


@api_view(['GET', 'POST', 'DELETE'])
def account_list(request):

    # Return all accounts
    # Expected body parameters: none
    if request.method == 'GET':
        accounts = Account.objects.all()
        account_serializer = AccountSerializer(accounts, many=True)
        response = JsonResponse(account_serializer.data, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        return response

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

    # Delete an account
    # Expected body parameters:
    #   - id
    if request.method == 'DELETE':
        account_id = request.GET.get('id', False)
        found_account = get_account_if_exist(account_id)

        if found_account.delete():
            return Response({'message': "Account deleted with success"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "Error 400, something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'HEAD'])
def account_detail(request, id):

    found_account = get_account_if_exist(id)

    # Return account's detail and his transactions (older firsts)
    # Add "X-Sistema-Bancario" header with following format: "name;surname"
    # Expected body parameters: none
    if request.method == 'GET':
        account_serializer = AccountSerializer(found_account)
        response = JsonResponse(account_serializer.data, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        set_name_surname_header(response, account_serializer)

        return response

    # Make a self transaction using "amount" parameter
    # if amount > 0 -> Deposit
    # if amount < 0 -> Withdraw
    # Expected body parameters:
    #   - amount
    if request.method == 'POST':
        amount = request.POST.get('amount', False)

        # It's a Self Deposit or Withdraw
        account_from = found_account
        account_to = found_account

        new_transaction = TransactionSerializer(
            data={
                'account_from': account_from.id,
                'account_to': account_to.id,
                'amount': amount
            })

        if new_transaction.is_valid(raise_exception=True):
            amount = new_transaction.validated_data.get('amount')

            if amount >= 0:
                account_to.deposit(abs(amount))
            else:
                account_to.withdrawal(abs(amount))
            new_transaction.save()

        return Response({"transaction_id": new_transaction.data['id'],
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

    # Divert a transaction using "transaction_id" parameter
    # Expected body parameters:
    #   - transaction_id
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', False)
        transaction = get_transaction_if_exist(transaction_id)

        if transaction.account_from is None or transaction.account_to is None:
            return Response({'message': 'Error 404, one of two accounts no longer exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            transaction_account_from = Account.objects.get(
                pk=transaction.account_from.id)
            transaction_account_to = Account.objects.get(
                pk=transaction.account_to.id)

        amount_to_divert = transaction.amount
        difference_between_amounts = transaction_account_to.balance - amount_to_divert

        if difference_between_amounts >= 0:
            transaction_account_from.deposit(amount_to_divert)
            transaction_account_to.withdrawal(amount_to_divert)

            new_transaction = Transaction.objects.create(
                account_from=transaction_account_to,
                account_to=transaction_account_from,
                amount=-amount_to_divert
            )

            new_transaction_serializer = TransactionSerializer(new_transaction)
        else:
            raise ValidationError(
                {'message': 'Error 400, Not enough money to divert'})

        return Response(new_transaction_serializer.data)
