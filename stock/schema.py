import graphene
from .types import AccountType, StockType, ResearchType
from .models import Account, Stock, Research
from .crypt import AESCipher
from graphql_jwt.decorators import login_required
from .views import getStockNamu
from django.db.models import Sum


# 유저로부터 증권사 아이디와 비밀번호 받기.
class GetAccountMutation(graphene.Mutation):
    class Arguments:
        company_id = graphene.String()
        company_secret = graphene.String()
        company = graphene.Int()

    account = graphene.Field(AccountType)

    @login_required
    def mutate(self, info, company=1, **kwargs):
        company_id = kwargs.get("company_id")
        company_secret = kwargs.get("company_secret")

        # 고객 정보 암호화
        company_id = AESCipher().encrypt_str(company_id)
        company_secret = AESCipher().encrypt_str(company_secret)

        user_id = info.context.user.id

        # 이미 등록된 계정이 있을 경우
        try:
            account = Account.objects.get(user_id=user_id, company=company)
            account.company_id = (
                company_id if company_id is not None else account.company_id
            )
            account.company_secret = (
                company_secret if company_secret is not None else account.company_secret
            )
            account.save()

            # 계정이 없다면 새로 만든다.
        except Account.DoesNotExist:
            account = Account.objects.create(
                user_id=user_id,
                company_id=company_id,
                company_secret=company_secret,
                company=company,
            )
            account.save()

        return GetAccountMutation(account=account)


# 증권 계좌 조회
class GetStockMutation(graphene.Mutation):
    class Arguments:
        click = graphene.Boolean()

    result = graphene.Boolean()

    @login_required
    def mutate(self, info, **kwargs):

        user_id = info.context.user.id
        account = Account.objects.get(user_id=user_id, company=1)

        # 복호화
        company_id = AESCipher().decrypt_str(account.company_id)
        company_secret = AESCipher().decrypt_str(account.company_secret)

        # 웹 스켈핑
        dic = getStockNamu(company_id, company_secret)
        if dic:
            # 기존 자료 삭제 후 재 생성.
            try:
                Stock.objects.filter(user_id=user_id, company="나무").delete()
                for code, value in dic.items():
                    stock = Stock.objects.create(
                        user_id=user_id,
                        code=code,
                        amount=value[1],
                        stockname=value[0],
                        company="나무",
                    )
                    stock.save()
                    result = True

            except Stock.DoesNotExist:
                for code, value in dic.items():
                    stock = Stock.objects.create(
                        user_id=user_id,
                        code=code,
                        amount=value[1],
                        stockname=value[0],
                        company="나무",
                    )
                    stock.save()
                    result = True
        else:
            result = False
            raise PermissionError("아이디와 비번을 다시 한번 확인 해주세요.")

        return GetStockMutation(result=result)


class Query(graphene.ObjectType):
    allstock = graphene.List(StockType)
    account = graphene.Field(AccountType)
    havestock = graphene.Field(StockType, code=graphene.String(required=True))
    totalAmount = graphene.String(code=graphene.String(required=True))
    allResearch = graphene.List(ResearchType, code=graphene.String(required=True))

    @login_required
    def resolve_allResearch(self, info, **kwargs):
        code = kwargs.get("code")
        return Research.objects.filter(code=code)

    @login_required
    def resolve_totalAmount(self, info, **kwargs):
        code = kwargs.get("code")
        totalAmount = Stock.objects.filter(code=code).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        return totalAmount

    @login_required
    def resolve_allstock(self, info, **kwargs):
        user = info.context.user
        stock = Stock.objects.filter(user_id=user.id)
        return stock

    @login_required
    def resolve_account(self, info, **kwargs):
        user = info.context.user
        account = Account.objects.get(user_id=user.id)
        return account

    @login_required
    def resolve_havestock(self, info, **kwargs):
        user = info.context.user
        code = kwargs.get("code")
        try:
            stock = Stock.objects.get(user_id=user.id, code=code)
            return stock
        except Stock.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    get_account = GetAccountMutation.Field()
    get_stock = GetStockMutation.Field()
