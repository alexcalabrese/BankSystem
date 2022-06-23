from django.http import JsonResponse
from .models.account import Account, get_account_if_exist
from .utils import validate_float_field
from .models.transaction import Transaction, get_transaction_if_exist
from .models.selfTransansaction import SelfTransaction
from .serializers import AccountSerializer, TransactionSerializer, SelfTransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, ParseError, NotFound
from django.shortcuts import render

def custom_not_found(response):
    return JsonResponse({"message": "Error 404, page not found"}, status=status.HTTP_404_NOT_FOUND, safe=False)

def set_name_surname_header(response, serializer):
    response['X-Sistema-Bancario'] = str(serializer['name'].value) + \
        ";" + str(serializer['surname'].value)

    return True


def render_home(request):
    return render(request, "homepage.html")


def render_transfer(request):
    return render(request, "transfer.html")


@api_view(['GET', 'POST', 'DELETE'])
def account_list(request):

    # Return all accounts
    # Expected body parameters: none
    if request.method == 'GET':
        accounts = Account.objects.filter(is_active=1)
        account_serializer = AccountSerializer(accounts, many=True)
        response = JsonResponse(account_serializer.data, safe=False)
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

        found_account.is_active = 0
        found_account.save()

        return Response({'message': "Account deleted with success"}, status=status.HTTP_204_NO_CONTENT)


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
        amount = request.data.get('amount', False)

        # It's a Self Deposit or Withdraw
        account = found_account

        new_transaction = SelfTransactionSerializer(
            data={
                'account': account.id,
                'amount': amount
            })

        if new_transaction.is_valid(raise_exception=True):
            amount = new_transaction.validated_data.get('amount')


            if amount >= 0:
                account.deposit(abs(amount))
            else:
                account.withdrawal(abs(amount))
            new_transaction.save()

        return Response({"transaction_id": new_transaction.data['id'],
                         "updated_balance": account.balance})

    # Overwrite "name" and "surname"
    # Expected body parameters:
    #   - name
    #   - surname
    if request.method == 'PUT':
        request_name = request.data.get('name', False)
        request_surname = request.data.get('surname', False)

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
        request_name = request.data.get('name', False)
        request_surname = request.data.get('surname', False)

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
        request_account_from = request.data.get('account_from', False)
        request_account_to = request.data.get('account_to', False)

        if request_account_from == request_account_to:
            account_from = get_account_if_exist(request_account_from)
            account_to = account_from
        else:
            if request_account_from == False or request_account_to == False:
                raise ValidationError(
                    {'message': 'Error 400, sender and receiver are required'})
            
            account_from = get_account_if_exist(request_account_from)
            account_to = get_account_if_exist(
                request_account_to)

        new_transaction = TransactionSerializer(data=request.data)

        if new_transaction.is_valid(raise_exception=True):
            amount = new_transaction.validated_data.get('amount')

            if amount < 0:
                raise ValidationError(
                    {'message': 'Error 400, cannot perform negative transfer'})

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
        transaction_id = request.data.get('id', False)
        transaction = get_transaction_if_exist(transaction_id)

        if transaction.account_from.is_active == 0 or transaction.account_to.is_active == 0:
            return Response({'message': 'Error 404, one of two accounts no longer exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            transaction_account_from = get_account_if_exist(
                transaction.account_from.id)
            transaction_account_to = get_account_if_exist(
                transaction.account_to.id)

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

            transaction.is_diverted = 1
            transaction.save()

            new_transaction_serializer = TransactionSerializer(new_transaction)
        else:
            raise ValidationError(
                {'message': 'Error 400, Not enough money to divert'})

        return Response(new_transaction_serializer.data)
