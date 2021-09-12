from graphene_django import DjangoObjectType
from .models import Account, Research, Stock


class AccountType(DjangoObjectType):
    class Meta:
        model = Account


class StockType(DjangoObjectType):
    class Meta:
        model = Stock


class ResearchType(DjangoObjectType):
    class Meta:
        model = Research
