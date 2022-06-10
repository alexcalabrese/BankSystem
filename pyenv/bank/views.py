from django.forms import ValidationError
from django.http import JsonResponse
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def account_list(request):

    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"accountId": serializer.data['id']}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'HEAD'])
def account_detail(request, id):

    try:
        account = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    if request.method == 'POST':
        try:
            account_from = Account.objects.get(pk=id)
            account_to = Account.objects.get(pk=id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        amount = float(request.POST.get('amount', False))

        if amount < 0 and abs(amount) > abs(account_from.balance):
            return Response({'Message': 'Not enough money'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            previus_balance = account_to.balance
            account_to.balance = (previus_balance + amount)
            account_to.save()

            self_transaction = Transaction.objects.create(
                account_from=account_from,
                account_to=account_to,
                amount=amount
            )
            serializer = TransactionSerializer(self_transaction)
            return Response({"transaction_id": serializer.data['id'], "updated_balance": account_to.balance})

    if request.method == 'PUT':
        request_name = request.POST.get('name', False)
        request_surname = request.POST.get('surname', False)

        if request_name != False:
            account.name = request_name

        if request_surname != False:
            account.surname = request_surname

        account.save()

        serializer = AccountSerializer(account)
        return Response(serializer.data)

    if request.method == 'PATCH':
        request_name = request.POST.get('name', False)
        request_surname = request.POST.get('surname', False)

        if request_name != False:
            account.name = request_name
        else:
            account.surname = request_surname

        account.save()

        serializer = AccountSerializer(account)
        return Response(serializer.data)

    if request.method == 'HEAD':
        response = Response(status=status.HTTP_200_OK)
        response['X-Sistema-Bancario'] = account.name + ";" + account.surname

        return response


@api_view(['POST'])
def new_transfer(request):

    if request.method == 'POST':
        account_from_id = str(request.POST.get('account_from_id', False))
        account_to_id = str(request.POST.get('account_to_id', False))

        try:
            account_from = Account.objects.get(pk=account_from_id)
            account_to = Account.objects.get(pk=account_to_id)
        except Account.DoesNotExist:
            return Response({'Message': 'Account does not exist'}, status=status.HTTP_404_NOT_FOUND)

        amount = float(request.POST.get('amount', False))

        if amount < 0:
            return Response({'Message': 'Cannot perform negative transfer'}, status=status.HTTP_400_BAD_REQUEST)
        elif amount > account_from.balance:
            return Response({'Message': 'Not enough money'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            account_from_previus_balance = account_from.balance
            account_from.balance = (account_from_previus_balance - amount)
            account_from.save()

            account_to_previus_balance = account_to.balance
            account_to.balance = (account_to_previus_balance + amount)
            account_to.save()

            transaction = Transaction.objects.create(
                account_from=account_from,
                account_to=account_to,
                amount=amount
            )

            transaction_serializer = TransactionSerializer(transaction)

            response = {"transaction_id": transaction_serializer.data['id']}
            response["account_from_id"] = ({"account_from_id": account_from.id,
                                            "updated_balance": account_from.balance})
            response["account_to_id"] = ({"account_to_id": account_to.id,
                                          "updated_balance": account_to.balance})

            return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def new_divert(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', False)

        try:
            transaction = Transaction.objects.get(pk=transaction_id)
        except ValidationError as error:
            return Response({'Message': error.messages[0]}, status=status.HTTP_404_NOT_FOUND)
        except Transaction.DoesNotExist:
            return Response({'Message': 'Transaction does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            transaction_account_from = Account.objects.get(
                pk=transaction.account_from.id)
            transaction_account_to = Account.objects.get(
                pk=transaction.account_to.id)
        except Account.DoesNotExist:
            return Response({'Message': 'One of two account no longer exist'}, status=status.HTTP_404_NOT_FOUND)

        reversed_amount = transaction.amount
        difference_between_amounts = transaction_account_to.balance - reversed_amount
        print("Differences: ", difference_between_amounts)

        if difference_between_amounts >= 0:
            account_from_previus_balance = transaction_account_from.balance
            account_to_previus_balance = transaction_account_to.balance

            transaction_account_from.balance = (
                account_from_previus_balance + reversed_amount)
            transaction_account_to.balance = (
                account_to_previus_balance - reversed_amount)

            transaction_account_from.save()
            transaction_account_to.save()

            new_transaction = Transaction.objects.create(
                account_from=transaction_account_to,
                account_to=transaction_account_from,
                amount=-reversed_amount
            )
        else:
            return Response({'Message': 'Not enough money to divert'}, status=status.HTTP_400_BAD_REQUEST)

        new_transaction_serializer = TransactionSerializer(new_transaction)
        return Response(new_transaction_serializer.data)
