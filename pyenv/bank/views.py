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


@api_view(['GET', 'POST', 'DELETE'])
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

        if amount < 0 and amount > account_from.balance:
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
            return Response(serializer.data)

    if request.method == 'DELETE':
        pass
