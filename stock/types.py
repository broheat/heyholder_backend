from graphene_django import DjangoObjectType
from .models import Account, Stock


class AccountType(DjangoObjectType):
    class Meta:
        model = Account

class StockType(DjangoObjectType):
    class Meta:
        model = Stock