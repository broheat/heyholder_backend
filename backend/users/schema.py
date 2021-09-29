import graphene
from users.types import UserType
from graphql_jwt.decorators import login_required


class AgreeMutaion(graphene.Mutation):
    class Arguments:
        agree_1 = graphene.Boolean()
        username = graphene.String()

    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, **kwargs):
        agree_1 = kwargs.get("agree_1")
        username = kwargs.get("username")
        user = info.context.user
        user.agree_1 = user.agree_1 if agree_1 is None else agree_1
        user.username = user.username if username is None else username
        user.save()
        return AgreeMutaion(user=user)


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserType)

    @login_required
    def resolve_whoami(self, info, **kwargs):
        user = info.context.user
        return user


class Mutation(graphene.ObjectType):
    agree = AgreeMutaion.Field()
