import graphene
from users.types import UserType
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required

class AgreeMutaion(graphene.Mutation):
    class Arguments:
        agree_1 = graphene.Boolean()
    
    user = graphene.Field(UserType)
    @login_required
    def mutate(self, info, **kwargs):
        agree_1 = kwargs.get('agree_1')
        r_user = info.context.user
        r_user.agree_1 = agree_1 if agree_1 != None else r_user.agree_1
        r_user.save()
        return AgreeMutaion(user=r_user)

class ChangeNameMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
    
    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, **kwargs):
        username = kwargs.get('username')
        r_user = info.context.user
        r_user.username = username if username != None else r_user.username
        r_user.name_change = True
        r_user.save()
        return ChangeNameMutation(user=r_user)

class Query(graphene.ObjectType):
    whoami = graphene.Field(UserType)

    @login_required
    def resolve_whoami(self, info, **kwargs):
        user = info.context.user
        return user

class Mutation(graphene.ObjectType):
    agree = AgreeMutaion.Field()
    name_change = ChangeNameMutation.Field()
